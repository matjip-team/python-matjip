# app/spring_client.py
import requests

from app.config import JAVA_BACKEND_URL


def send_to_spring(data):
    res = requests.post(
        f"{JAVA_BACKEND_URL}/api/spring/restaurants/import",
        json=data
    )
    res.raise_for_status()
