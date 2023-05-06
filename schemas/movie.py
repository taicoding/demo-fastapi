from pydantic import BaseModel, Field
from typing import Optional, List


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    year: int = Field(gt=2000, lt=2024)
    rating: float = Field(gt=0, le=10)
    category: str = Field(max_length=15, min_length=5)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Avatar",
                "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
                "year": "2009",
                "rating": 7.8,
                "category": "Acción",
            }
        }
