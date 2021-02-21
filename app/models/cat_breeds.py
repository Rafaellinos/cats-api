from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Float,
)
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.database import metadata
from app.config.settings import get_settings

settings = get_settings()

cat_breeds = Table(
    "cat_breeds",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("public_id", UUID(), default=uuid.uuid4, unique=True),
    Column("breed", String, nullable=False),
    Column("location_origin", String),
    Column("coat_length", Float),
    Column("body_type", String),
    Column("pattern", String),
)
