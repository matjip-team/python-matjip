# 1. 베이스 이미지
FROM python:3.12-slim

# 2. 환경 변수
ENV PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# 3. 필수 OS 패키지 (빌드용)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# 4. Poetry 2.3.1 설치 (공식 스크립트 사용)
RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.3.1

# 설치 확인 (빌드 로그용)
RUN poetry --version

# 5. 작업 디렉토리 생성
WORKDIR /app

# 6. 의존성 파일 복사
COPY pyproject.toml poetry.lock* /app/

# 7. 가상환경 없이 설치, dev dependencies 제외 (Poetry 2.x 문법 적용)
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-ansi

# 8. 앱 소스 복사
COPY . /app

# 9. FastAPI 포트 노출
EXPOSE 8000

# 10. FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]