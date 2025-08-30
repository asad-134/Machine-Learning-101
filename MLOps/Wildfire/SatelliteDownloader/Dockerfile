# Use the official Azure Functions Python image as a base
FROM mcr.microsoft.com/azure-functions/python:4-python3.11-core-tools

# Set the working directory inside the container
WORKDIR /workspace

# Copy the requirements.txt file first (for better Docker caching)
COPY requirements.txt .

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# ⭐⭐⭐ CRITICAL: Add this line ⭐⭐⭐
CMD ["func", "start", "--python"]