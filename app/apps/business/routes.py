import logging
import uuid
from typing import TypeVar

from fastapi import Request
from fastapi_mongo_base.models import BusinessEntity
from fastapi_mongo_base.routes import AbstractBaseRouter
from fastapi_mongo_base.schemas import BusinessEntitySchema, PaginatedResponse
from server.config import Settings
from usso.fastapi import jwt_access_security

from .models import Business
from .schemas import BusinessDataCreateSchema, BusinessDataUpdateSchema, BusinessSchema

T = TypeVar("T", bound=BusinessEntity)
TS = TypeVar("TS", bound=BusinessEntitySchema)


class BusinessRouter(AbstractBaseRouter[Business, BusinessSchema]):
    def __init__(self):
        super().__init__(
            model=Business,
            schema=BusinessSchema,
            user_dependency=jwt_access_security,
            prefix="/businesses",
        )

    def config_schemas(self, schema, **kwargs):
        super().config_schemas(schema, **kwargs)

        self.create_request_schema = BusinessDataCreateSchema
        self.update_request_schema = BusinessDataUpdateSchema

    def config_routes(self, **kwargs):
        super().config_routes(**kwargs)

    async def list_items(
        self,
        request: Request,
        offset: int = 0,
        limit: int = 10,
        origin: str = None,
        name: str = None,
        user_id: uuid.UUID = None,
        uid: uuid.UUID = None,
    ):
        t_user_id = await self.get_user_id(request)
        if t_user_id != Settings.USSO_USER_ID:
            if origin or name or uid:
                user_id = None
            else:
                user_id = t_user_id
        limit = max(1, min(limit, Settings.page_max_limit))

        logging.info(f"list_items: {user_id=} {origin=} {name=} {uid=}")
        items, total = await self.model.list_total_combined(
            user_id=user_id,
            offset=offset,
            limit=limit,
            domain=origin,
            name=name,
            uid=uid,
        )

        items_in_schema = [self.list_item_schema(**item.model_dump()) for item in items]
        logging.info(f"list_items: {items_in_schema=}")
        return PaginatedResponse(
            items=items_in_schema,
            total=total,
            offset=offset,
            limit=limit,
        )

    async def create_item(
        self,
        request: Request,
        item: BusinessDataCreateSchema,
    ):
        return await super().create_item(request, item.model_dump())

    async def update_item(
        self,
        request: Request,
        uid: uuid.UUID,
        data: BusinessDataUpdateSchema,
    ):
        return await super().update_item(
            request, uid, data.model_dump(exclude_none=True)
        )


router = BusinessRouter().router
