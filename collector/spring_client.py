# app/spring_client.py
import requests

def send_to_spring(data):
    res = requests.post(
        "http://localhost:8081/api/restaurants/import",
        json=data
    )
    res.raise_for_status()
