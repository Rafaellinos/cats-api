from databases import Database
from sqlalchemy import create_engine, MetaData

from app.config.settings import get_settings

settings = get_settings()

# SQLAlchemy
engine = create_engine(settings.DATABASE_URL)
metadata = MetaData()

# databases query builder
database = Database(settings.DATABASE_URL)
