from fastapi import FastAPI
from app.api import user
from fastapi.middleware.cors import CORSMiddleware
from app.api.recommend import router as recommend_router
from app.config import CORS_ALLOWED_ORIGINS

app = FastAPI(
    title="AI Restaurant Recommendation API",
    description="카카오 지도 + AI 기반 맛집 추천 서비스",
    version="1.0.0"
)

# 🔥 CORS 허용 설정 (React/Java 연결용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 테스트
@app.get("/api/fastapi")
async def root():
    return {"message": "AI Recommendation Server Running"}

@app.get("/api/fastapi/health")
def health():
    return {"status": "UP"}


# AI 추천 API 연결
app.include_router(recommend_router)
app.include_router(user.router)