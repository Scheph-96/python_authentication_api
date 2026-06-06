from sqlalchemy import create_engine

from app.core.config import Settings

engine = create_engine("", echo=Settings.ENV == "development")