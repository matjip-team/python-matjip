import httpx
from app.config import KAKAO_API_KEY

url = "https://dapi.kakao.com/v2/local/search/keyword.json"
headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

async def search_places(location: str, food: str):
    query = f"{location} {food}".strip()
    if not query:
        return []

    params = {
        "query": query,
        "category_group_code": "FD6",
        "size": 10,
        "sort": "accuracy"
    }

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.get(url, headers=headers, params=params)
        res.raise_for_status()
        data = res.json()

        return [
            {
                "name": p.get("place_name"),
                "address": p.get("road_address_name") or p.get("address_name"),
                "lat": float(p.get("y")),
                "lng": float(p.get("x")),
                "category": p.get("category_name"),
            }
            for p in data.get("documents", [])
        ]
    except:
        return [{
            "name": "기본 맛집",
            "address": "서울",
            "lat": 37.5,
            "lng": 127.0,
            "category": food or "음식점"
        }]
