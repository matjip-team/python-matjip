import re
import httpx
from app.config import KAKAO_API_KEY, PEXELS_API_KEY

url = "https://dapi.kakao.com/v2/local/search/keyword.json"
headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

# 카카오 장소 페이지 요청 시 브라우저처럼 보이게 (일부 서버는 봇 차단)
KAKAO_PLACE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


async def get_place_image_from_kakao_page(place_url: str) -> str | None:
    """place.map.kakao.com 장소 페이지에서 og:image(대표 이미지) URL 추출. 실패 시 None."""
    if not place_url or "place.map.kakao.com" not in place_url:
        return None
    try:
        async with httpx.AsyncClient(timeout=8, follow_redirects=True) as client:
            res = await client.get(place_url, headers=KAKAO_PLACE_HEADERS)
            res.raise_for_status()
            html = res.text
    except Exception:
        return None
    # og:image 메타 태그 추출 (공유 시 사용하는 대표 이미지)
    m = re.search(
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        html,
    ) or re.search(
        r'property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        html,
    )
    if m:
        url = m.group(1).strip()
        if url.startswith("http"):
            return url
    return None


async def get_place_image_url(place_name: str, category: str) -> str | None:
    """장소 이름/카테고리로 Pexels에서 음식·맛집 관련 이미지 URL 1개 반환. API 키 없으면 None."""
    if not PEXELS_API_KEY:
        return None
    query = f"{place_name} {category} restaurant food".strip()[:80]
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.get(
                "https://api.pexels.com/v1/search",
                params={"query": query, "per_page": 1, "orientation": "landscape"},
                headers={"Authorization": PEXELS_API_KEY},
            )
            res.raise_for_status()
            data = res.json()
            photos = data.get("photos") or []
            if not photos:
                res2 = await client.get(
                    "https://api.pexels.com/v1/search",
                    params={"query": "restaurant food korea", "per_page": 1, "orientation": "landscape"},
                    headers={"Authorization": PEXELS_API_KEY},
                )
                res2.raise_for_status()
                photos = (res2.json()).get("photos") or []
            if photos:
                src = photos[0].get("src") or {}
                return src.get("large") or src.get("medium") or src.get("original")
    except Exception:
        pass
    return None

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
                "place_url": p.get("place_url"),
                "phone": p.get("phone"),
            }
            for p in data.get("documents", [])
        ]
    except:
        return [{
            "name": "기본 맛집",
            "address": "서울",
            "lat": 37.5,
            "lng": 127.0,
            "category": food or "음식점",
            "place_url": None,
            "phone": None,
        }]
