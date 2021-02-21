from pydantic import BaseModel, Field
from typing import Optional


class CatBreeds(BaseModel):
    breed: str = Field(..., title="Breed Name", min_length=5, max_length=50)
    location_origin: Optional[str] = Field(None, title="Location", min_length=3)
    coat_length: Optional[float] = Field(0.00, title="Coat Length", gt=0.00)
    body_type: Optional[str] = Field(None, title="Body Type", min_length=3)
    pattern: Optional[str] = Field(None, title="Pattern", min_length=3)


class CatBreedsIn(CatBreeds):
    ...


class CatBreedsOut(CatBreeds):
    public_id: str = Field(..., title="ID")
