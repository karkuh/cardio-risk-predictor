# Cardio Risk Predictor

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1CZ_FB19g6zkNjezxyTV6iZHahfj37DvN?usp=sharing)

An end-to-end Machine Learning project designed to predict heart disease risk. This repository includes both the link to **model training pipeline** and an **interactive web dashboard** for real-time diagnostics.

## 📌 Project Overview

This project consists of two main components:
1.  **Training Pipeline:** Automated data fetching, cleaning, EDA, and model training optimizing for **Recall**.
2.  **Interactive Dashboard:** A user-friendly Streamlit web app that allows doctors or users to input medical data and get an instant risk assessment with visual feedback.

## 🌟 Dashboard Features

* **Real-time Prediction:** Instant analysis of patient data.
* **Visual Risk Levels:**
    * 🟢 **Safe:** Low probability (<50%), celebrated with balloons.
    * 🟡 **Warning:** Medium risk (<80%), advice to consult a doctor.
    * 🔴 **Danger:** High risk (>80%), alert animation (Ambulance).
* **Interactive Form:** Easy-to-use inputs for age, blood pressure, cholesterol, etc.

## 🛠 Tech Stack

* **Core:** Python 3.x
* **Machine Learning:** Scikit-learn, Joblib
* **Data Processing:** Pandas, NumPy
* * **Web Framework:** Streamlit
* **Visualization:** Matplotlib, Seaborn, Lottie (Animations)
