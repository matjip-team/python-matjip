import random
from app.services.tag_service import infer_place_tags
from app.services.user_service import get_user_preferences

async def calculate_place_score(place: dict, analysis: dict) -> float:
    score = 0
    tags = infer_place_tags(place)

    if analysis.get("food") and analysis["food"] in place.get("category", ""):
        score += 5

    if analysis.get("mood") == "분위기 좋은":
        if "감성" in tags:
            score += 4
        if "데이트" in tags:
            score += 3

    if analysis.get("user_id"):
        prefs = await get_user_preferences(analysis["user_id"])
        if analysis.get("food") in prefs.get("likedFoods", []):
            score += 2

    score += random.uniform(0, 1)
    return round(score, 2)
