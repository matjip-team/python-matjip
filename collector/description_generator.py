import random


def generate_description(category: str, address: str | None) -> str:
    region = address.split()[0] if address else "도심"

    # 🔥 카테고리별 문장 구조 완전 분리
    if category == "한식":
        templates = [
            f"{region}에 위치한 한식 전문 매장으로 정성스럽게 준비된 메뉴를 제공합니다.",
            f"{region}에서 든든한 한식을 즐길 수 있는 곳으로 많은 방문객이 찾고 있습니다.",
            f"{region} 지역에서 집밥 같은 한식을 맛볼 수 있는 매장입니다."
        ]

    elif category == "양식":
        templates = [
            f"{region}에 위치한 분위기 좋은 양식 레스토랑입니다.",
            f"{region}에서 파스타와 스테이크 등 다양한 양식 메뉴를 즐길 수 있습니다.",
            f"{region} 데이트 코스로 추천할 만한 양식 전문 매장입니다."
        ]

    elif category == "고기/구이":
        templates = [
            f"{region}에서 신선한 고기와 구이 메뉴를 즐길 수 있는 매장입니다.",
            f"{region} 지역에서 고기 맛집으로 알려진 곳입니다.",
            f"{region}에서 숯불구이와 다양한 고기 요리를 제공하는 전문점입니다."
        ]

    elif category == "씨푸드":
        templates = [
            f"{region}에 위치한 신선한 해산물 요리 전문 매장입니다.",
            f"{region}에서 다양한 해산물 메뉴를 즐길 수 있는 곳입니다.",
            f"{region} 지역에서 회와 해물 요리로 인기 있는 매장입니다."
        ]

    elif category == "비건":
        templates = [
            f"{region}에 위치한 건강한 비건 메뉴 전문 매장입니다.",
            f"{region}에서 채식 중심의 식사를 즐길 수 있는 곳입니다.",
            f"{region} 지역에서 웰빙 식단을 제공하는 비건 매장입니다."
        ]

    elif category == "카페/디저트":
        templates = [
            f"{region}에 위치한 감성적인 카페입니다.",
            f"{region}에서 커피와 디저트를 함께 즐기기 좋은 공간입니다.",
            f"{region} 지역에서 여유로운 시간을 보내기 좋은 카페입니다."
        ]

    else:  # 일중/세계음식
        templates = [
            f"{region}에서 다양한 세계 음식을 즐길 수 있는 매장입니다.",
            f"{region}에 위치한 글로벌 푸드 전문점입니다.",
            f"{region} 지역에서 색다른 해외 요리를 경험할 수 있는 곳입니다."
        ]

    return random.choice(templates)
