from typing import List
from pymongo.database import Database
from pymongo.collection import Collection
from mongodb_orm.types.index import Index
from mongodb_orm.types.options import Options
from mongodb_orm.types.Relation import Relation
from mongodb_orm.singletons.mongodb_singleton_client import MongoDBClient


class BaseMongoDBModel:
    """
        Preventing direct Instantiation of this class
    """

    def __new__(cls, *args, **kwargs):
        if cls is BaseMongoDBModel:
            raise TypeError(f"only children of '{cls.__name__}' may be instantiated")
        return object.__new__(cls)

    def connect(self, tenant: str, collection: str, options: Options = None, indexes: List[Index] = None,
                relations: List[Relation] = None) -> Collection:
        client = MongoDBClient().get_database(f'{tenant}')
        if collection not in client.list_collection_names():
            self._create_collection(client, collection, options, indexes, relations)
        return client.get_collection(collection)

    """
        Creating the collection if not exists and if there are indexes they will be created
    """

    @staticmethod
    def _create_collection(client: Database, collection: str, options: Options = None,
                           indexes: List[Index] = None, relations: List[Relation] = None) -> None:
        schema: dict = {}
        if options is not None:
            schema = {'$jsonSchema': options['schema']}
        collection_instance = client.create_collection(collection,
                                                       timeseries={'timeField': 'created_at',
                                                                   'metaField': 'consumed'} if options and options.get(
                                                           'time_series') else None,
                                                       validator=schema if options and not options.get(
                                                           'time_series') else None,
                                                       expireAfterSeconds=30 if options and options.get(
                                                           'time_series') else None)
        if indexes:
            for index in indexes:
                collection_instance.create_index([
                    (index['name'], 1 if index['asc'] else -1)
                ],
                    unique=index['unique'] if options and not options.get('time_series') else None,
                    expireAfterSeconds=index['expireAfterSeconds'] if index['expireAfterSeconds'] else None
                )
