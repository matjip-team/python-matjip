import requests
import os
from urllib.parse import urlparse

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# 신뢰 가능한 출처
ALLOWED_DOMAINS = [
    "map.kakao.com",
    "map.naver.com",
    "pcmap.place.naver.com",
    "menupan.com",
    "diningcode.com",
    "img.siksinhot.com",
]

# 이미 사용한 이미지 URL 추적(중복 방지)
USED_IMAGES = set()

def is_valid_image(url: str) -> bool:
    if not url:
        return False

    domain = urlparse(url).netloc
    if not any(allowed in domain for allowed in ALLOWED_DOMAINS):
        return False

    if url in USED_IMAGES:
        return False

    return True


def search_image(name: str, address: str) -> str | None:
    url = "https://openapi.naver.com/v1/search/image"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }

    # 🔥 실전에서 잘 먹히는 검색어 순서
    queries = [
        f"{name}",
        f"{name} 후기",
        f"{name} 메뉴",
        f"{name} 방문",
        f"{name} {address.split()[0]}",
        f"{name} 매장",
        f"{name} 외관",
        f"{name} 간판",
        f"{name} 음식점",
    ]

    for query in queries:
        params = {
            "query": query,
            "display": 10,
            "sort": "sim",
        }

        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()

        items = res.json().get("items", [])
        for item in items:
            image_url = item.get("link")

            if is_valid_image(image_url):
                USED_IMAGES.add(image_url)
                return image_url

    return None
