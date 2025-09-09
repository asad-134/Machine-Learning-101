import azure.functions as func
import logging
import planetary_computer as pc
from pystac_client import Client
from azure.storage.blob import BlobServiceClient
import json
import os
import time  # Added for timing
from datetime import datetime
app = func.FunctionApp()

@app.route(route="download_scene", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def download_scene(req: func.HttpRequest) -> func.HttpResponse:
    total_start_time = time.time()
    logging.info('Python HTTP trigger function started processing a request.')
    
    # 1. CHECK ENVIRONMENT VARIABLE
    env_start = time.time()
    connection_string = os.environ.get("AzureWebJobsStorage")
    if not connection_string:
        logging.error("AzureWebJobsStorage environment variable is not set")
        return func.HttpResponse("AzureWebJobsStorage environment variable is not set", status_code=500)
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    env_time = time.time() - env_start
    logging.info(f"Environment setup completed in {env_time:.2f} seconds")

    # 2. GET THE PARAMETERS FROM THE REQUEST
    try:
        json_start = time.time()
        req_body = req.get_json()
        area_of_interest = req_body.get('area_of_interest')
        date = req_body.get('date')
        max_cloud_cover = req_body.get('max_cloud_cover', 10)
        region = req_body.get('region', 'manifests')
        json_time = time.time() - json_start
        logging.info(f"JSON parsing completed in {json_time:.2f} seconds")
        logging.info(f"Parameters - Area: {area_of_interest}, Date: {date}, Max clouds: {max_cloud_cover}%")
        
    except ValueError as e:
        logging.error(f"JSON parsing failed: {str(e)}")
        return func.HttpResponse("Invalid JSON in request body.", status_code=400)

    # 3. SEARCH THE PLANETARY COMPUTER CATALOG
    try:
        catalog_start = time.time()
        logging.info("Starting STAC catalog search...")
        catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            intersects=area_of_interest,
            datetime=date,
            query={"eo:cloud_cover": {"lt": max_cloud_cover}}
        )
        catalog_time = time.time() - catalog_start
        logging.info(f"STAC catalog setup completed in {catalog_time:.2f} seconds")

        items_start = time.time()
        items = list(search.get_items())
        items_time = time.time() - items_start
        logging.info(f"STAC items retrieval completed in {items_time:.2f} seconds. Found {len(items)} images.")

        if not items:
            logging.warning("No satellite images found for the given criteria")
            return func.HttpResponse("No satellite images found for your criteria.", status_code=404)

    except Exception as e:
        logging.error(f"STAC search failed: {str(e)}")
        return func.HttpResponse(f"STAC search error: {str(e)}", status_code=500)

    # 4. FIND BEST ITEM AND SIGN URL
    try:
        best_item_start = time.time()
        best_item = min(items, key=lambda item: item.properties['eo:cloud_cover'])
        best_item_time = time.time() - best_item_start
        logging.info(f"Best item selection completed in {best_item_time:.2f} seconds. Cloud cover: {best_item.properties['eo:cloud_cover']}%")

        sign_start = time.time()
        signed_item = pc.sign(best_item)
        sign_time = time.time() - sign_start
        logging.info(f"URL signing completed in {sign_time:.2f} seconds")

    except Exception as e:
        logging.error(f"Item processing failed: {str(e)}")
        return func.HttpResponse(f"Item processing error: {str(e)}", status_code=500)

    # 5. BUILD MANIFEST
    try:
        manifest_start = time.time()
        asset = signed_item.assets["visual"]
        manifest = {
            "scene_id": best_item.id,
            "date": best_item.datetime.isoformat(),
            "cloud_cover": best_item.properties['eo:cloud_cover'],
            "image_url": asset.href,
            "area_of_interest": area_of_interest
        }
        manifest_time = time.time() - manifest_start
        logging.info(f"Manifest creation completed in {manifest_time:.2f} seconds")

    except Exception as e:
        logging.error(f"Manifest creation failed: {str(e)}")
        return func.HttpResponse(f"Manifest error: {str(e)}", status_code=500)

    # 6. UPLOAD TO BLOB STORAGE
    try:
        upload_start = time.time()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"raw/satellite/{region}/{best_item.id}_{timestamp}_manifest.json"
        blob_client = blob_service_client.get_blob_client(container="wildfire-data", blob=blob_name)
        blob_client.upload_blob(json.dumps(manifest), overwrite=True)
        upload_time = time.time() - upload_start
        logging.info(f"Blob upload completed in {upload_time:.2f} seconds. Saved to: {blob_name}")

    except Exception as e:
        logging.error(f"Blob upload failed: {str(e)}")
        return func.HttpResponse(f"Upload error: {str(e)}", status_code=500)

    # 7. FINAL RESPONSE
    total_time = time.time() - total_start_time
    logging.info(f"TOTAL FUNCTION EXECUTION TIME: {total_time:.2f} seconds")
    
    return func.HttpResponse(
        json.dumps({
            "manifest_path": blob_name, 
            "status": "success",
            "execution_time": total_time
        }),
        status_code=200,
        mimetype="application/json"
    )
