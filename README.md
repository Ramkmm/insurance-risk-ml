# 🏠 Insurance Housing Risk Prediction System

## 📌 Overview

This project is an end-to-end Machine Learning application that predicts housing insurance risk based on property details. It integrates ML modeling, API development, and a user-friendly dashboard.

---

## 🚀 Features

* Predict insurance risk score
* Recommend premium amount
* Real-time prediction via API
* Interactive Streamlit dashboard
* Deployed on AWS EC2 using Docker

---

## 🧠 ML Model

* Algorithm: Random Forest / XGBoost
* Features:

  * House Age
  * Location Risk
  * Roof Type
  * Past Claims
  * Property Value

---

## 🏗️ Architecture

User → Streamlit UI → FastAPI → ML Model → Prediction

---

## 🌐 Live Application

### 🔹 FastAPI (Backend)

http://54.164.81.44:8000/docs

### 🔹 Streamlit (Frontend)

http://54.164.81.44:8501

---

## 🐳 Docker Deployment

### Build Image

docker build -t insurance-app .

### Run Container

docker run -d -p 8000:8000 -p 8501:8501 insurance-app

---

## ☁️ AWS Deployment

* EC2 Instance (Ubuntu)
* Docker containerized application
* Elastic IP for static access
* Security Groups configured for ports 8000 & 8501
* Auto start/stop using EventBridge Scheduler

---

## 📊 Example API Request

POST /predict

```json
{
  "house_age": 10,
  "location_risk": 0.5,
  "roof_type": 2,
  "past_claims": 1,
  "property_value": 500000
}
```

---

## 📈 Output

```json
{
  "risk_score": 0.63,
  "recommended_premium": 520.5,
  "risk_category": "Medium Risk"
}
```

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Streamlit
* Scikit-learn
* Docker
* AWS EC2

---

## 💡 Future Improvements

* Add authentication
* Use AWS Lambda for lightweight inference
* CI/CD pipeline (GitHub Actions)
* Domain + HTTPS support

---

## 👨‍💻 Author

Rambabu Vaddeboina

---

## ⭐ If you like this project, give it a star!
