from uuid import uuid4
from app.models.cat_breeds import cat_breeds
from app.models.schemas.cat_breeds import (
    CatBreedsIn,
)
from app.database.database import database


async def get_cat_breeds(breeds: CatBreedsIn):
    query = (
        cat_breeds
        .select()
        .where(
            cat_breeds.c.breed.like(f"%{breeds.breed}%"),
        )
    )
    result = await database.execute(query=query)
    return result


async def get_all_breeds():
    query = cat_breeds.select()
    result = await database.fetch_all(query)
    return [
        {k: str(v) for k, v in line.items()}
        for line in result
    ]


async def post_cat_breed(breed_values: CatBreedsIn):
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


async def put_cat_breed(public_id: str, breed_values: CatBreedsIn):
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
    )
    result = await database.execute(query)
    return result


async def delete_cat_breed(public_id: int):
    query = cat_breeds.delete.where(
        public_id == cat_breeds.c.public_id,
    )
    result = await database.execute(query=query)
    return result
