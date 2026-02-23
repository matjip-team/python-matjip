import os
from dotenv import load_dotenv

load_dotenv()

# True: 운영 환경, False: 개발 환경 (기본)
PRODUCTION = os.getenv("PRODUCTION", "false").lower() in ("true", "1", "yes")

# Java(Spring) 백엔드 API Base URL: 로컬 = localhost:8081, 운영 = 43.202.121.6
JAVA_BACKEND_URL = "http://43.202.121.6" if PRODUCTION else "http://localhost:8081"

# CORS 허용 Origin
# 개발: localhost (React, Java)
# 운영: 아래 리스트 또는 CORS_ALLOWED_ORIGINS 환경변수(쉼표 구분)로 오버라이드
CORS_ORIGINS_DEV = [
    "http://localhost:5173",  # React 개발 서버
    "http://localhost:8081",  # Java 개발 서버
]
CORS_ORIGINS_PROD = [
    "http://43.202.121.6",   # 운영 프론트엔드 URL로 변경
    "http://43.202.121.6",    # 운영 백엔드 URL로 변경 (필요 시)
]

if PRODUCTION:
    _origins_str = os.getenv("CORS_ALLOWED_ORIGINS")
    if _origins_str:
        CORS_ALLOWED_ORIGINS = [o.strip() for o in _origins_str.split(",") if o.strip()]
    else:
        CORS_ALLOWED_ORIGINS = CORS_ORIGINS_PROD
else:
    CORS_ALLOWED_ORIGINS = CORS_ORIGINS_DEV

AI_API_KEY = os.getenv("AI_API_KEY")
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")
# Pexels API (무료): 장소별 이미지 검색용, 없으면 이미지 생략
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")