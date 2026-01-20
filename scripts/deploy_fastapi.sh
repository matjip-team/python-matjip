#!/bin/bash

IMAGE=xxx0209/fastapi-backend:latest
GREEN_PORT=8001

echo "Pull latest FastAPI image..."
docker pull $IMAGE

echo "Run green FastAPI container..."
docker run -d --name fastapi-green -p ${GREEN_PORT}:8000 $IMAGE

echo "Health checking FastAPI..."
SUCCESS=false
for i in {1..10}; do
  STATUS=$(curl -s http://localhost:${GREEN_PORT}/health | jq -r .status)
  if [[ "$STATUS" == "UP" ]]; then
    SUCCESS=true
    echo "Health Check passed on attempt #$i"
    break
  fi
  echo "Waiting for FastAPI... ($i)"
  sleep 3
done

if [[ "$SUCCESS" != true ]]; then
  echo "FastAPI health check failed. Rollback."
  docker stop fastapi-green
  docker rm fastapi-green
  exit 1
fi

echo "Switching containers..."
docker stop fastapi-blue 2>/dev/null || true
docker rm fastapi-blue 2>/dev/null || true

docker rename fastapi-green fastapi-blue

echo "FastAPI deployment successful!"