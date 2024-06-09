from pydantic_settings import BaseSettings
import os

class Setting(BaseSettings):
    # Database config
    database_url: str
    database_name: str
    database_user: str
    database_password: str
    database_port: str

# path = os.getenv("../.env")
# setting = Setting(_env_file=path, _env_file_encoding="utf-8")
setting = Setting()