import httpx

from app.config import JAVA_BACKEND_URL


async def get_user_preferences(user_id: int):
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            res = await client.get(f"{JAVA_BACKEND_URL}/users/{user_id}/preferences")
        return res.json()
    except:
        return {}
