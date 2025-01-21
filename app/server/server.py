from apps.business.routes import router as business_router
from fastapi_mongo_base.core import app_factory

from . import config

app = app_factory.create_app(
    settings=config.Settings(), origins=["http://localhost:8000"], ufaas_handler=False
)
app.include_router(business_router, prefix=f"{config.Settings.base_path}")
