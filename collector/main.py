# collector/main.py
from fastapi import FastAPI
from collector.collector import collect_places

app = FastAPI(title="Matjip Collector API")

@app.post("/collect")
def collect():
    keywords = [
        # 한식
        "강남역 한식",

        # 카페
        "성수 카페",

        # 고기/구이
        "강남역 삼겹살",
        "홍대 곱창",

        # 씨푸드
        "노량진 횟집",
        "강남역 초밥",

        # 비건
        "이태원 샐러드",
        "성수 플랜트",

        # 세계음식
        "이태원 태국음식",
        "이태원 멕시칸"
    ]

    data = collect_places(keywords)

    return {
        "count": len(data),
        "data": data
    }
