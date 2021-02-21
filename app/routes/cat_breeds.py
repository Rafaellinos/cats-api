from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.services import cat_breeds
from app.models.schemas.cat_breeds import (
    CatBreedsOut,
    CatBreedsIn,
)

router = APIRouter()


@router.get("/cat-breed/{breed}", response_model=List[CatBreedsOut])
async def get_cat_breed(
        breeds: CatBreedsIn = Depends(),
):
    result = await cat_breeds.get_cat_breeds(breeds)
    return result


@router.get("/cat-breed", response_model=List[CatBreedsOut])
async def get_all_breeds():
    result = await cat_breeds.get_all_breeds()
    return result


@router.post("/cat-breed", status_code=201)
async def post_cat_breed(
        breed: CatBreedsIn,
):
    result = await cat_breeds.post_cat_breed(breed)
    return {
        "public_id": result,
    }


@router.put(
    "/cat-breed/{id}",
    response_model=CatBreedsOut,
    response_model_exclude_unset=True,
)
async def put_cat_breed(
        id: str,  # TODO avoid override builtin
        breed: CatBreedsIn,
):
    result = await cat_breeds.put_cat_breed(id, breed)
    if not result:
        raise HTTPException(status_code=404, detail="breed not found")
    return {
        "breed": result.breed,
        "location_origin": result.location_origin,
        "coat_length": result.coat_length,
        "body_type": result.body_type,
        "pattern": result.pattern,
    }


@router.delete(
    "/cat-breed/{id}",
)
async def delete_cat_breed(
        id: str,
):
    result = await cat_breeds.delete_cat_breed(id)
    if not result:
        raise HTTPException(status_code=404, detail="breed not found")
    return {
        "message": "Breed deleted successfully!",
    }




