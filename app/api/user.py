from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user_optional

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me")
def get_me(user=Depends(get_current_user_optional)):
    return {"user": user}
