# 🏠 Insurance Housing Risk Prediction System

## 📌 Overview

This project is an end-to-end **Machine Learning application** that predicts housing insurance risk based on property details.

It integrates:

* 📊 ML Model (Risk Prediction)
* ⚡ FastAPI (Backend API)
* 🎨 Streamlit (Frontend UI)
* 🐳 Docker (Containerization)
* ☁️ AWS EC2 (Cloud Deployment)
* 🌐 Nginx + Domain + SSL (Production Setup)
* 🔁 GitHub Actions (CI/CD Automation)

---

## 🚀 Live Application

### 🌐 Frontend (Streamlit UI)

👉 https://houseinsurancerisk.site

### ⚡ API (FastAPI Docs)

👉 https://houseinsurancerisk.site/docs

### 🔮 Prediction API Endpoint

👉 https://houseinsurancerisk.site/api/predict

---

## 🧠 Architecture

```
User → Streamlit UI → Nginx → FastAPI → ML Model → Prediction
```

---

## ⚙️ Tech Stack

* Python
* Scikit-learn / XGBoost
* FastAPI
* Streamlit
* Docker & Docker Compose
* AWS EC2 (Ubuntu)
* Nginx (Reverse Proxy)
* SSL (HTTPS)
* GitHub Actions (CI/CD)

---

## 🔁 CI/CD Pipeline

Automated deployment workflow:

```
Local Development → GitHub Push → GitHub Actions → EC2 → Docker Restart → Live Update
```

✔ No manual SSH required
✔ Auto deployment on every push
✔ Production-ready workflow

---

## 🐳 Docker Deployment

### Build Image

```
docker build -t insurance-app .
```

### Run Container

```
docker run -d -p 8000:8000 -p 8501:8501 insurance-app
```

---

## ☁️ AWS Deployment

* EC2 Ubuntu Instance
* Dockerized application
* Elastic IP mapped to domain
* Nginx reverse proxy configured
* SSL enabled (HTTPS)
* Security groups: 80, 443 open

---

## 📡 Example API Request

### POST /predict

```json
{
  "house_age": 10,
  "location_risk": 0.5,
  "roof_type": 1,
  "past_claims": 1,
  "property_value": 500000
}
```

### Response

```json
{
  "risk_score": 0.0006,
  "recommended_premium": 501.27,
  "risk_category": "Low Risk"
}
```

---

## 📊 Features

✔ Real-time risk prediction
✔ Premium calculation
✔ Feature importance visualization
✔ Interactive Streamlit dashboard
✔ Production deployment with domain
✔ CI/CD automation

---

## 🔐 Security Notes

* API served via HTTPS
* Nginx reverse proxy handling traffic
* SSH access secured using `.pem` key
* GitHub secrets used for CI/CD deployment

---

## 👨‍💻 Author

**Rambabu Vaddeboina**

---

## ⭐ Future Improvements

* Add user authentication
* Store predictions in database
* Add monitoring (Prometheus/Grafana)
* Scale using Kubernetes

---
