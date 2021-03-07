from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.services import cat_breeds
from app.services.errors import BreedAlreadyExists
from app.models.schemas.cat_breeds import (
    CatBreeds,
    CatBreedsOut,
    CatBreedsIn,
    CatBreedsSearch,
)

router = APIRouter()


@router.get("/cat-breed", response_model=List[CatBreedsOut])
async def get_cat_breeds(
        breeds: CatBreedsSearch = Depends(),
):
    result = await cat_breeds.get_cat_breeds(breeds)
    return result


@router.get("/cat-breed/{public_id}", response_model=CatBreedsOut)
async def get_cat_breed(
        public_id: str,
):
    result = await cat_breeds.get_cat_breed_by_id(public_id)
    if not result:
        raise HTTPException(status_code=404, detail='Cat Breed not found :(')
    return result


@router.post("/cat-breed", status_code=201)
async def post_cat_breed(
        breed: CatBreedsIn,
):
    try:
        result = await cat_breeds.post_cat_breed(breed)
    except BreedAlreadyExists:
        raise HTTPException(status_code=409, detail="Breed already exists")
    return {
        "public_id": result,
    }


@router.put(
    "/cat-breed/{public_id}",
    response_model=CatBreedsOut,
    response_model_exclude_unset=True,
)
async def put_cat_breed(
        public_id: str,
        breed: CatBreedsIn,
):
    try:
        result = await cat_breeds.put_cat_breed(public_id, breed)
    except BreedAlreadyExists:
        raise HTTPException(status_code=409, detail="Breed already exists")
    if not result:
        raise HTTPException(status_code=404, detail="breed not found")
    return {
        "breed": result.breed,
        "location_origin": result.location_origin,
        "coat_length": result.coat_length,
        "body_type": result.body_type,
        "pattern": result.pattern,
    }


@router.patch(
    "/cat-breed/{public_id}",
)
async def patch_cat_breed(
        public_id: str,
        breed: CatBreeds,
):
    update_data = breed.dict(exclude_unset=True)
    try:
        return await cat_breeds.patch_cat_breed(public_id, update_data)
    except BreedAlreadyExists:
        raise HTTPException(status_code=409, detail="Breed already exists")


@router.delete(
    "/cat-breed/{public_id}",
)
async def delete_cat_breed(
        public_id: str,
):
    result = await cat_breeds.delete_cat_breed(public_id)
    if not result:
        raise HTTPException(status_code=404, detail="breed not found")
    return {
        "message": "Breed deleted successfully!",
    }




