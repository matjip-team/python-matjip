from fastapi import FastAPI

app = FastAPI()

@app.get("/api/fastapi")
async def root():
    return {"message": "Hello World"}

@app.get("/api/fastapi/health")
def health():
    return {"status": "UP"}
