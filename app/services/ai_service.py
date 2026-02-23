from openai import OpenAI
from app.config import AI_API_KEY

client = OpenAI(api_key=AI_API_KEY)

FOODS = ["고기", "치킨", "파스타", "햄버거", "초밥", "술집", "카페", "피자"]


def analyze_question(question: str) -> dict:
    food = next((f for f in FOODS if f in question), None)

    location = question
    if food:
        location = location.replace(food, "")

    location = (
        location.replace("맛집", "")
        .replace("추천해줘", "")
        .replace("추천", "")
        .strip()
    )

    mood = "분위기 좋은" if "분위기" in question or "감성" in question else None

    return {"location": location, "food": food, "mood": mood}


def generate_rule_based_comment(question: str, places: list):
    if not places:
        return "조건에 맞는 맛집을 찾지 못했어요 😢"

    names = ", ".join([p["name"] for p in places[:2]])

    if "분위기" in question or "감성" in question:
        return f"{names}는 분위기가 좋아서 데이트나 모임에 추천드려요 ✨"

    if any(food in question for food in FOODS):
        return f"{names}가 요청하신 메뉴에 잘 맞는 맛집이에요 🍽️"

    return f"{names}는 평점과 리뷰가 좋아 추천드려요 👍"


def generate_place_description(name: str, address: str, category: str) -> str:
    """가게 이름·주소·카테고리로 1~2문장 소개 문구 생성 (AI 또는 템플릿)."""
    if not name:
        return "AI가 추천한 맛집이에요. 카카오맵에서 메뉴·리뷰를 확인해 보세요."

    if AI_API_KEY:
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 맛집 소개를 여러 문장으로 소개하는 역활입니다. 한국어로만 답하고, 이모지 사용하지 마세요.",
                    },
                    {
                        "role": "user",
                        "content": f"다음 맛집을 여러 문장으로 소개해 주세요. 이름: {name}, 주소: {address}, 카테고리: {category}",
                    },
                ],
                max_tokens=150,
            )
            text = (completion.choices[0].message.content or "").strip()
            if text:
                return text
        except Exception:
            pass

    return f"{name}은(는) {category} 맛집이에요.\r\n{address}에 위치해 있어요.\r\n카카오맵에서 메뉴와 리뷰를 확인해 보세요."
