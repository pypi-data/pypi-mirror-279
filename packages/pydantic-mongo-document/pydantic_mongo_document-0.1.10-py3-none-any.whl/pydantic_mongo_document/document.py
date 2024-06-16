from typing import Annotated, Any, ClassVar, List, Optional, Self, Type

import bson
import pymongo
import pymongo.errors
import pymongo.results
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
from pydantic import (
    AfterValidator, AnyUrl, BaseModel, BeforeValidator, Field, UrlConstraints,
    validate_call,
)
from pymongo.collection import Collection
from pymongo.database import Database

from pydantic_mongo_document.encoder import JsonEncoder
from pydantic_mongo_document.exceptions import DocumentNotFound

UNSET = object()


class ReplicaConfig(BaseModel):
    """Mongodb replica config model."""

    uri: Annotated[
        AnyUrl,
        UrlConstraints(allowed_schemes=["mongodb", "mongodb+srv"]),
        Field(..., description="Mongodb connection URI."),
    ]
    client_options: dict[str, Any] = Field(
        default_factory=dict,
        description="Mongodb client options.",
    )


class Document(BaseModel):
    __primary_key__: ClassVar[str] = "id"

    __config__: ClassVar[dict[str, ReplicaConfig]] = {}
    """Map of replicas to mongo URIs."""

    __replica__: ClassVar[str]
    """Mongodb replica name."""

    __database__: ClassVar[str]
    """Mongodb database name."""

    __collection__: ClassVar[str]
    """Mongodb collection name."""

    __clients__: ClassVar[dict[str, AsyncIOMotorClient]] = {}
    """Map of clients for each database."""

    __document__: dict
    """Document data. For internal use only."""

    NotFoundError: ClassVar[Type[Exception]] = DocumentNotFound
    DuplicateKeyError: ClassVar[Type[Exception]] = pymongo.errors.DuplicateKeyError

    encoder: ClassVar[JsonEncoder] = JsonEncoder()

    id: str = Field(default_factory=lambda: str(bson.ObjectId()), alias="_id")

    def model_post_init(self, __context: Any) -> None:
        self.__document__ = self.model_dump(by_alias=True, exclude_none=True)
        print(self.__document__)

    @property
    def primary_key(self) -> Any:
        return getattr(self, self.__primary_key__)

    @classmethod
    def get_replica_config(cls) -> ReplicaConfig:
        return cls.__config__[cls.__replica__]

    @property
    def primary_key_field_name(self) -> str:
        return self.model_fields[self.__primary_key__].alias or self.__primary_key__

    @classmethod
    @validate_call
    def set_replica_config(cls, config: dict[str, ReplicaConfig]) -> None:
        cls.__config__ = config

    @classmethod
    def client(cls) -> AsyncIOMotorClient:
        if cls.__replica__ not in cls.__clients__:
            cls.__clients__[cls.__replica__] = AsyncIOMotorClient(
                host=str(cls.get_replica_config().uri),
                **cls.get_replica_config().client_options,
            )

        return cls.__clients__[cls.__replica__]

    @classmethod
    def sync_client(cls) -> pymongo.MongoClient[Any]:
        return pymongo.MongoClient(str(cls.get_replica_config().uri))

    @classmethod
    def database(cls) -> AsyncIOMotorDatabase:
        return cls.client()[cls.__database__]

    @classmethod
    def sync_database(cls) -> Database[Any]:
        return cls.sync_client()[cls.__database__]

    @classmethod
    def collection(cls) -> AsyncIOMotorCollection:
        return cls.database()[cls.__collection__]

    @classmethod
    def sync_collection(cls) -> Collection[Any]:
        return cls.sync_database()[cls.__collection__]

    @classmethod
    async def create_indexes(cls) -> None:
        """Creates indexes for collection."""

    @classmethod
    async def one(
        cls,
        document_id: str | None = None,
        add_query: dict[str, Any] | None = None,
        required: bool = True,
        **kwargs: Any,
    ) -> Optional[Self]:
        """Finds one document by ID."""

        query = {}
        if document_id is not None:
            query["_id"] = document_id
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        result = await cls.collection().find_one(query, **kwargs)

        if result is not None:
            return cls.model_validate(result)

        if required:
            raise cls.NotFoundError()

        return None

    @classmethod
    async def all(
        cls,
        document_ids: List[str | bson.ObjectId] | None = None,
        add_query: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> List[Self]:
        """Finds all documents based in IDs."""

        query = {}
        if document_ids is not None:
            query["_id"] = {"$in": document_ids}
        if add_query is not None:
            query.update(add_query)

        documents = []

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        cursor = cls.collection().find(query, **kwargs)
        async for document in cursor:
            documents.append(cls.model_validate(document))

        return documents

    @classmethod
    async def count(cls, add_query: Optional[dict[str, Any]] = None, **kwargs: Any) -> int:
        """Counts documents in collection."""

        query = {}
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        return await cls.collection().count_documents(query, **kwargs)

    async def delete(self) -> pymongo.results.DeleteResult:
        """Deletes document from collection."""

        query = self.encoder.encode_dict(
            {self.primary_key_field_name: self.primary_key},
        )

        return await self.collection().delete_one(query)

    async def commit_changes(self, fields: Optional[List[str]] = None) -> None:
        """Saves changed document to collection

        :param fields: Field names (by alias).
        """

        search_query: dict[str, Any] = {self.primary_key_field_name: self.primary_key}
        update_query: dict[str, Any] = {}

        if not fields:
            fields = [field for field in self.model_fields.keys() if field != self.__primary_key__]

        data = self.encoder.encode_dict(
            self.model_dump(by_alias=True, exclude_none=True),
            reveal_secrets=True,
        )

        for field in fields:
            if field in data and data[field] != self.__document__.get(field):
                update_query.setdefault("$set", {}).update({field: data[field]})
            elif field not in data and field in self.__document__:
                update_query.setdefault("$unset", {}).update({field: ""})

        if update_query:
            await self.collection().update_one(search_query, update_query)

    async def insert(self) -> Self:
        """Inserts document into collection."""

        obj = await self.collection().insert_one(
            self.encoder.encode_dict(
                self.model_dump(by_alias=True, exclude_none=True),
                reveal_secrets=True,
            )
        )

        if getattr(self, self.__primary_key__, None) is None:
            setattr(self, self.__primary_key__, obj.inserted_id)

        return self


def check_object_id(value: str) -> str:
    if not bson.ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return str(value)


ObjectId = Annotated[str, BeforeValidator(check_object_id)]
