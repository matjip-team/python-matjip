# 1. 베이스 이미지
FROM python:3.12-slim

# 2. 작업 디렉토리 생성
WORKDIR /app

# 3. Poetry 설치
RUN pip install --no-cache-dir poetry

# 4. 의존성 파일 복사
COPY pyproject.toml poetry.lock* /app/

# 5. 의존성 설치 (가상환경 없이 설치)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 6. 앱 소스 복사
COPY . /app

EXPOSE 8000
# 7. FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]