# --- 1단계: 빌더 (Builder) ---
FROM python:3.12-slim AS builder

# 환경 변수 설정
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

# 빌드에만 필요한 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.3.1

WORKDIR /app
COPY pyproject.toml poetry.lock* README.md* /app/

# 의존성 설치 (가상환경 없이 시스템에 직접 설치)
RUN poetry install --only main --no-interaction --no-ansi --no-root

# --- 2단계: 실행기 (Runner) ---
FROM python:3.12-slim AS runner

# 필수 환경 변수만 유지
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 빌더 단계에서 설치된 라이브러리들만 쏙 빼오기 (핵심!)
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 소스 코드 복사
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]