import requests

url = "http://127.0.0.1:8000/predict"

data = {
    "house_age": 12,
    "location_risk": 0.6,
    "roof_type": 2,
    "past_claims": 1,
    "property_value": 450000
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())