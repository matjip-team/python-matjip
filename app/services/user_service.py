import httpx

async def get_user_preferences(user_id: int):
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            res = await client.get(f"http://localhost:8080/users/{user_id}/preferences")
        return res.json()
    except:
        return {}
