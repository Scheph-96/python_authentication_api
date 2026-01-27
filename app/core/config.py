from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
settings = Settings()