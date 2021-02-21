from fastapi import APIRouter

from .cat_breeds import router

router_ = APIRouter()
router_.include_router(router, tags=["cat-breeds"])
