from fastapi import APIRouter, Depends
from app.models.schemas import (
    RecommendRequest,
    RecommendResponse,
    PlaceDetailsRequest,
    PlaceDetailsResponse,
)
from app.services.place_service import (
    search_places,
    get_place_image_url,
    get_place_image_from_kakao_page,
)
from app.services.recommendation_service import calculate_place_score
from app.services.auth_service import get_current_user_optional
from app.services.ai_service import (
    analyze_question,
    generate_rule_based_comment,
    generate_place_description,
)

router = APIRouter(prefix="/api/fastapi/recommend", tags=["AI Recommendation"])


@router.post("/", response_model=RecommendResponse)
async def recommend(
    data: RecommendRequest,
    user=Depends(get_current_user_optional)
):
    print("🔥 USER:", user)
    print("🎯 Preferred Categories:", data.preferredCategories)

    # 1️⃣ 질문 분석
    analysis = analyze_question(data.question)

    # 2️⃣ 장소 검색
    places = await search_places(
        analysis["location"],
        analysis["food"] or ""
    )

    preferred_categories = data.preferredCategories or []

    # 3️⃣ 점수 계산
    for p in places:
        p["score"] = await calculate_place_score(
            place=p,
            analysis=analysis,
            preferred_categories=preferred_categories
        )

    # 4️⃣ 정렬
    sorted_places = sorted(places, key=lambda x: x["score"], reverse=True)

    # 5️⃣ 멘트 생성
    comment = generate_rule_based_comment(data.question, sorted_places)

    return {
        "analysis": analysis,
        "recommended_places": sorted_places[:5],
        "ai_comment": comment
    }


@router.post("/place-details", response_model=PlaceDetailsResponse)
async def get_place_details(data: PlaceDetailsRequest):
    """가게 이름·주소·카테고리로 소개 문구(AI)와 이미지 URL 조회.
    이미지는 1) 카카오 장소 페이지(place_url) og:image → 2) Pexels 순으로 시도."""
    description = generate_place_description(
        data.name.strip(),
        (data.address or "").strip(),
        (data.category or "").strip(),
    )
    image_url = None
    if data.place_url and "place.map.kakao.com" in data.place_url:
        image_url = await get_place_image_from_kakao_page((data.place_url or "").strip())
    if not image_url:
        image_url = await get_place_image_url(
            (data.name or "").strip(),
            (data.category or "").strip(),
        )
    return PlaceDetailsResponse(description=description, image_url=image_url)
