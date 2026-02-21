from collector.kakao_client import search_places
from collector.naver_image_client import search_image
from collector.description_generator import generate_description


SERVICE_CATEGORY_MAP = {
    "한식": ["한식", "백반", "국밥", "찌개", "전골"],
    "양식": [
        "양식", "이탈리안", "파스타", "스테이크", "프렌치",
        "브런치", "피자", "리조또", "바베큐", "그릴", "펍"
    ],
    "고기/구이": [
        "고기", "구이", "삼겹살", "갈비", "소고기", "돼지고기",
        "숯불", "바베큐", "불고기", "차돌", "곱창", "막창", "대창"
    ],
    "씨푸드": [
        "해산물", "회", "조개", "생선", "초밥",
        "스시", "횟집", "대게", "킹크랩", "랍스터",
        "조개구이", "해물탕", "해물찜"
    ],
    "일중/세계음식": [
        "일식", "중식", "아시아", "태국", "베트남",
        "세계", "분식", "퓨전", "아메리칸", "멕시칸"
    ],
    "비건": [
        "비건", "채식", "베지", "비건식당", "플랜트",
        "샐러드", "웰빙", "오가닉"
    ],
    "카페/디저트": ["카페", "커피", "디저트", "베이커리"]
}

DEFAULT_CATEGORY = "일중/세계음식"


def map_category(raw_category: str) -> str:
    if not raw_category:
        return DEFAULT_CATEGORY

    raw = raw_category.replace(" ", "")

    for service_category, keywords in SERVICE_CATEGORY_MAP.items():
        for keyword in keywords:
            if keyword in raw:
                return service_category

    parts = [p.strip() for p in raw_category.split(">")]
    for part in parts:
        for service_category, keywords in SERVICE_CATEGORY_MAP.items():
            for keyword in keywords:
                if keyword in part:
                    return service_category

    return DEFAULT_CATEGORY


def collect_places(keywords):
    results = []
    seen_external_ids = set()

    CATEGORY_LIMIT = {
        "한식": 20,
        "카페/디저트": 20,
        "양식": 15,
        "고기/구이": 15,
        "씨푸드": 15,
        "비건": 10,
        "일중/세계음식": 15
    }

    category_count = {k: 0 for k in CATEGORY_LIMIT.keys()}

    for keyword in keywords:
        for page in range(1, 2):  # 1페이지만 수집
            places = search_places(keyword, page)

            if not places:
                break

            for p in places:
                external_id = p["id"]

                # 중복 방지
                if external_id in seen_external_ids:
                    continue

                category = map_category(p.get("category_name", ""))

                # 카테고리 제한
                if category_count.get(category, 0) >= CATEGORY_LIMIT.get(category, 0):
                    continue

                name = p["place_name"]
                address = p.get("road_address_name") or p.get("address_name")

                # 이미지 요청 (429 방지 위해 순차 처리)
                try:
                    image_url = search_image(name, address)
                except Exception as e:
                    print("[IMAGE FAIL]", e)
                    image_url = None

                # 설명 자동 생성
                description = generate_description(category, address)

                phone = p.get("phone") or None

                results.append({
                    "external_id": external_id,
                    "name": name,
                    "address": address,
                    "lat": float(p["y"]),
                    "lng": float(p["x"]),
                    "category": category,
                    "image_url": image_url,
                    "description": description,
                    "phone": phone,
                    "source": "KAKAO"
                })

                seen_external_ids.add(external_id)
                category_count[category] += 1

    return results
