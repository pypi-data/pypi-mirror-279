import datetime
from typing import Union, cast, List, Dict, Any

import motor
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from sirius import common
from sirius.common import DataClass
from sirius.constants import EnvironmentSecret

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def initialize() -> None:
    global client, db
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"{common.get_environmental_secret(EnvironmentSecret.MONGO_DB_CONNECTION_STRING)}&retryWrites=false",
                                                    uuidRepresentation="standard") if client is None else client
    db = client[common.get_environmental_secret(EnvironmentSecret.APPLICATION_NAME)] if db is None else db


async def drop_collection(collection_name: str) -> None:
    await initialize()
    await cast(AsyncIOMotorDatabase, db).drop_collection(collection_name)


class DatabaseDocument(DataClass):
    id: ObjectId | None = None
    updated_timestamp: datetime.datetime | None = None
    created_timestamp: datetime.datetime | None = None

    @classmethod
    async def _get_collection(cls) -> AsyncIOMotorCollection:
        await initialize()
        global db
        return db[cls.__name__]

    async def save(self) -> None:
        collection: AsyncIOMotorCollection = await self._get_collection()

        if self.id is None:
            self.created_timestamp = datetime.datetime.now()
            object_id: ObjectId = (await collection.insert_one(self.model_dump(exclude={"id"}))).inserted_id
            self.__dict__.update(self.model_dump(exclude={"id"}))
            self.id = object_id
        else:
            self.updated_timestamp = datetime.datetime.now()
            await collection.replace_one({"_id": self.id}, self.model_dump(exclude={"id"}))

    async def delete(self) -> None:
        await initialize()
        collection: AsyncIOMotorCollection = await self._get_collection()
        await collection.delete_one({'_id': self.id})

    @classmethod
    def get_model_by_raw_data(cls, raw_data: Dict[Any, Any]) -> "DatabaseDocument":
        object_id = raw_data.pop("_id")
        queried_object: DatabaseDocument = cls(**raw_data)
        queried_object.id = object_id
        return queried_object

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> Union["DatabaseDocument", None]:
        await initialize()
        collection: AsyncIOMotorCollection = await cls._get_collection()
        object_model: Dict[str, Any] = await collection.find_one({'_id': object_id})
        return None if object_model is None else cls.get_model_by_raw_data(object_model)

    @classmethod
    async def find_by_query(cls, database_document: "DatabaseDocument", query_limit: int = 100) -> List["DatabaseDocument"]:
        collection: AsyncIOMotorCollection = await cls._get_collection()
        cursor = collection.find(database_document.model_dump(exclude={"id"}, exclude_none=True))
        return [cls.get_model_by_raw_data(document) for document in await cursor.to_list(length=query_limit)]
