# app/kakao_client.py
import requests
import os

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

BASE_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

def search_places(keyword: str, page: int = 1, size: int = 15):
    if page > 45:
        return []
    if not KAKAO_REST_API_KEY:
        raise RuntimeError("KAKAO_REST_API_KEY 환경변수가 설정되지 않았습니다")

    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"
    }

    params = {
        "query": keyword,
        "page": page,
        "size": size
    }

    res = requests.get(BASE_URL, headers=headers, params=params)
    res.raise_for_status()

    return res.json()["documents"]
