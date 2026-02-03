from fastapi import Cookie
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "this-is-a-secure-very-long-secret-key-1234567890"
ALGORITHM = "HS256"

def get_current_user_optional(accessToken: str | None = Cookie(default=None)):
    if accessToken is None:
        return None

    try:
        payload = jwt.decode(accessToken, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "email": payload.get("sub"),
            "userId": payload.get("userId"),
        }

    except ExpiredSignatureError:
        print("⛔ JWT 만료됨")
        return None

    except InvalidTokenError:
        print("⛔ 잘못된 JWT")
        return None
