from fastapi import APIRouter, Depends
from app.models.schemas import RecommendRequest, RecommendResponse
from app.services.place_service import search_places
from app.services.recommendation_service import calculate_place_score
from app.services.auth_service import get_current_user_optional
from app.services.ai_service import analyze_question, generate_rule_based_comment

router = APIRouter(prefix="/recommend", tags=["AI Recommendation"])


@router.post("/", response_model=RecommendResponse)
async def recommend(
    data: RecommendRequest,
    user=Depends(get_current_user_optional)
):
    print("🔥 USER:", user)

    # 1️⃣ 질문 분석
    analysis = analyze_question(data.question)

    # 2️⃣ 장소 검색
    places = await search_places(
        analysis["location"],
        analysis["food"] or ""
    )

    # 3️⃣ 점수 계산
    for p in places:
        p["score"] = await calculate_place_score(p, analysis)

        # 🔥 로그인 사용자 개인화 확장 위치
        if user:
            p["score"] += 1.5  # 예시 가중치

    # 4️⃣ 정렬
    sorted_places = sorted(places, key=lambda x: x["score"], reverse=True)

    # 5️⃣ 멘트 생성
    comment = generate_rule_based_comment(data.question, sorted_places)

    return {
        "analysis": analysis,
        "recommended_places": sorted_places[:5],
        "ai_comment": comment
    }
