from typing import TypeVar, Generic, Type, Any, Optional

from fastapi import HTTPException, status
import sqlalchemy
from pydantic import BaseModel

from db.session import database


ModelType = TypeVar("ModelType", bound=sqlalchemy.Table)
SchemaModelType = TypeVar("SchemaModelType", bound=sqlalchemy.Table)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: Any) -> Optional[ModelType]:
        query = self.model.select().where(self.model.c.id == id)
        return await database.fetch_one(query)

    async def get_all(self, *, filter: Optional[Any] = None) -> Optional[ModelType]:
        query = self.model.select()
        if filter is not None:
            query = query.where(filter)
        return await database.fetch_all(query)

    async def get_or_404(self, *, id: Any) -> Optional[ModelType]:
        response = await self.get(id)
        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return response

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        query = self.model.insert()
        created_id = await database.execute(query=query, values=obj_in.dict())
        if created_id is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return await self.get(id=created_id)

    async def update(self, *, id: Any, obj_in: CreateSchemaType) -> ModelType:
        query = self.model.update().where(self.model.c.id == id).values(**obj_in.dict())
        response = await database.execute(query)
        if response == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        query = self.model.select().where(self.model.c.id == id)
        response = await database.fetch_one(query)
        return response

    async def remove(self, *, id: Any) -> bool:
        query = self.model.delete().where(self.model.c.id == id)
        response = await database.execute(query)
        if response == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return True
