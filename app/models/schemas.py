from pydantic import BaseModel
from typing import List, Dict, Optional

class RecommendRequest(BaseModel):
    question: str
    userId: Optional[int] = None
    preferredCategories: Optional[List[str]] = []

class Place(BaseModel):
    name: str
    address: str
    lat: float
    lng: float
    category: str
    score: float

class RecommendResponse(BaseModel):
    analysis: Dict
    recommended_places: List[Dict]
    ai_comment: str


class PlaceDetailsRequest(BaseModel):
    name: str
    address: str = ""
    category: str = ""
    place_url: Optional[str] = None  # 카카오 장소 페이지 URL 있으면 여기서 대표 이미지 시도


class PlaceDetailsResponse(BaseModel):
    description: str
    image_url: Optional[str] = None