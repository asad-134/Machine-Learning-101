# Phishing Detection Web App

## Overview

This project is a **machine learning-based phishing detection web app** designed to classify URLs as either **phishing** or **legitimate**. It utilizes multiple machine learning models and a streamlined user interface built with **Streamlit**.

## Machine Learning Models Used

- **Random Forest**
- **Gradient Boosting**
- **Naïve Bayes**
- **Support Vector Machine (SVM)**

## Selected Features (ANOVA)

Feature selection was performed using ANOVA, and the following features were chosen for optimal model performance:

- `nb_www`
- `ratio_digits_url`
- `domain_in_title`
- `google_index`
- `page_rank`

## How It Works

1. The trained machine learning model processes input URL features.
2. It predicts whether the URL is **phishing** or **safe** based on the selected features.
3. The app displays the result in a user-friendly interface.

## Technologies Used

- **Python**
- **Scikit-Learn**
- **Streamlit**
- **Joblib (for model persistence)**

## Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/phishing-detection.git
   ```
2. Navigate to the project folder:
   ```bash
   cd phishing-detection
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Future Improvements

- Expand feature set for higher accuracy
- Integrate real-time URL analysis
- Deploy as a web service

Contributions are welcome! Feel free to fork, enhance, and submit pull requests. 🚀

