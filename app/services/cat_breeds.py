from uuid import uuid4
from sqlalchemy import and_
from asyncpg.exceptions import DataError

from app.models.cat_breeds import cat_breeds
from app.models.schemas.cat_breeds import (
    CatBreedsIn,
    CatBreedsOut,
    CatBreedsSearch,
)
from app.database.database import database
from .errors import BreedAlreadyExists


async def get_breed_by_name(breed: str):
    query = (
        cat_breeds
        .select()
        .where(
            cat_breeds.c.breed == breed,
        )
    )
    return await database.fetch_all(query)


async def ensure_unique_breed(breed: str) -> None:
    found = await get_breed_by_name(breed)
    if found:
        raise BreedAlreadyExists


async def get_cat_breeds(breeds: CatBreedsSearch):
    query = cat_breeds.select()

    if breeds.breed:
        query.append_whereclause(
            and_(
                cat_breeds.c.breed.ilike(f'%{breeds.breed}%'),
            )
        )

    if breeds.coat_length:
        query.append_whereclause(
            and_(
                cat_breeds.c.coat_length == breeds.coat_length,
            )
        )

    if breeds.location_origin:
        query.append_whereclause(
            and_(
                cat_breeds.c.location_origin.ilike(f'%{breeds.location_origin}%')
            )
        )

    if breeds.body_type:
        query.append_whereclause(
            and_(
                cat_breeds.c.breed.ilike(f"%{breeds.body_type}%")
            )
        )

    if breeds.pattern:
        query.append_whereclause(
            and_(
                cat_breeds.c.breed.ilike(f"%{breeds.pattern}%")
            )
        )

    result = await database.fetch_all(query=query)
    return [
        {k: str(v) for k, v in line.items()}
        for line in result
    ]


async def get_cat_breed_by_id(breed_id: str) -> dict:
    query = (
        cat_breeds
        .select()
        .where(
            cat_breeds.c.public_id == breed_id,
        )
    )
    try:
        result = await database.fetch_one(query=query)
    except DataError:
        return {}
    return {k: str(v) for k, v in result.items()}


async def post_cat_breed(breed_values: CatBreedsIn):
    await ensure_unique_breed(breed_values.breed)
    query = (
        cat_breeds
        .insert()
        .values(
            breed=breed_values.breed,
            location_origin=breed_values.location_origin,
            coat_length=breed_values.coat_length,
            body_type=breed_values.body_type,
            pattern=breed_values.pattern,
            public_id=uuid4(),
        )
        .returning(
            cat_breeds.c.public_id,
        )
    )
    return await database.execute(query)


async def patch_cat_breed(public_id: str, breed_values: dict):
    if breed_values.get("breed"):
        await ensure_unique_breed(breed_values.get("breed"))
    query = (
        cat_breeds
        .update()
        .where(
            public_id == cat_breeds.c.public_id,
        )
        .values(
            **breed_values,
        )
        .returning(
            cat_breeds.c.breed,
            cat_breeds.c.public_id,
            cat_breeds.c.location_origin,
            cat_breeds.c.coat_length,
            cat_breeds.c.body_type,
            cat_breeds.c.pattern,
        )
    )
    return await database.execute(query)


async def put_cat_breed(public_id: str, breed_values: CatBreedsIn):
    await ensure_unique_breed(breed_values.breed)
    query = (
        cat_breeds
        .update()
        .where(
            public_id == cat_breeds.c.public_id,
        )
        .values(
            breed=breed_values.breed,
            location_origin=breed_values.location_origin,
            coat_length=breed_values.coat_length,
            body_type=breed_values.body_type,
            pattern=breed_values.pattern,
        )
        .returning(
            cat_breeds.c.breed,
            cat_breeds.c.public_id,
            cat_breeds.c.location_origin,
            cat_breeds.c.coat_length,
            cat_breeds.c.body_type,
            cat_breeds.c.pattern,
        )
    )
    result = await database.execute(query)
    return result


async def delete_cat_breed(public_id: str):
    query = cat_breeds.delete.where(
        public_id == cat_breeds.c.public_id,
    )
    return await database.execute(query=query)
