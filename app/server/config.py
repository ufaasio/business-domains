"""FastAPI server configuration."""

import dataclasses
import os
from pathlib import Path

import dotenv
from fastapi_mongo_base.core import config

dotenv.load_dotenv()


@dataclasses.dataclass
class Settings(config.Settings):
    """Server config settings."""

    base_dir: Path = Path(__file__).resolve().parent.parent
    base_path: str = "/api/v1/apps/business"
    USSO_USER_ID: str = os.getenv("USSO_USER_ID")
