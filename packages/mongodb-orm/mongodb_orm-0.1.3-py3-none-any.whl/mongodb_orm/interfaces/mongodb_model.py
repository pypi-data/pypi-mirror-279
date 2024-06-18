import math
import pymongo
from bson import ObjectId
from datetime import datetime
from typing import List, Union, Sequence

from pymongo.command_cursor import CommandCursor
from pymongo.cursor import Cursor
from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from mongodb_orm.interfaces.mongodb_model_events import MongoDBModelEvents
from mongodb_orm.types.index import Index
from mongodb_orm.utils.helpers import Helper
from mongodb_orm.types.options import Options
from mongodb_orm.types.Relation import Relation
from mongodb_orm.decorators.chained import chained
from mongodb_orm.exceptions.syntax_exceptions import ChainingError
from mongodb_orm.interfaces.base_mongodb_model import BaseMongoDBModel


class MongoDBModel(BaseMongoDBModel, MongoDBModelEvents):
    """
        Public class variables to be overridden by the model
    """
    collection_name: str = ''
    # Check the following link to check what are the possible valid options for collection creation
    # https://www.mongodb.com/docs/manual/reference/method/db.createCollection/
    options: Options = None
    timestamp: bool = True
    # List[index] of the indexes for a
    indexes: List[Index] = None
    # List of the attributes allowed to be returned per query
    attributes: List[str] = ['*']
    # List of the attributes guarded against returned per query
    guarded: List[str] = []
    # List of the relationship to a model
    relations: List[Relation] = None

    """
        Preventing direct Instantiation of this class 
    """

    def __new__(cls, *args, **kwargs):
        if cls is MongoDBModel:
            raise TypeError(f"only children of '{cls.__name__}' may be instantiated")
        return object.__new__(cls)

    """
        The logic behind all the crud of a model
    """

    _collection: Collection = None

    def set_tenant(self, tenant_name: str):
        self.__init__(tenant=tenant_name)

    def __init__(self, tenant: str = 'public', **kwargs):
        self._collection = self.connect(tenant, self.collection_name, self.options, self.indexes, self.relations)
        self._projection = {k: 1 for k in self.attributes if k != '*' and k not in self.guarded}
        self._result: Cursor | InsertOneResult | dict | None = None
        self.chained = True

    def get_collection(self) -> Collection:
        return self._collection

    def query(self) -> 'MongoDBModel':
        self.chained = False
        return self

    def json(self) -> List[dict] | dict:
        if self._result is None:
            raise ChainingError(message='you can not call json directly, it needs to be chained')
        if isinstance(self._result, Cursor):
            return [Helper.standardize_dict(item, underscore=True) for item in list(self._result)]
        else:
            return Helper.standardize_dict(self._result, underscore=True)

    @chained
    def get(self, pk: str) -> Union[dict, 'MongoDBModel']:
        return self._collection.find_one({'_id': ObjectId(pk)}, projection=self._projection)

    @chained
    def get_all(self,
                filters: dict = None,
                page: int = 1,
                per_page: int = 10,
                sort_by: tuple = None) -> Union[dict, 'MongoDBModel']:
        sort_criteria: Sequence = [('_id', pymongo.ASCENDING)]

        if sort_by is not None:
            sort_criteria: Sequence = [sort_by]
        cursor: Cursor = self._collection.find(
            filters, projection=self._projection
        ).sort(sort_criteria).skip(
            (page * per_page) - per_page
        ).limit(per_page)
        # Convert cursor to list of dictionaries
        data = [Helper.standardize_dict(item, underscore=True) for item in list(cursor)]
        # Get total documents that matches the filters
        matches = self.count(filters)
        # Get total documents count
        total_documents = self.count()
        # Calculate total pages
        total_pages = math.ceil(total_documents / per_page)

        query_result: dict = {
            'data': data,
            'filters': filters,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'sort_by': [{sort_tuple[0]: sort_tuple[1]} for sort_tuple in sort_criteria],
            'matches': matches,
            'total_documents': total_documents
        }
        return query_result

    @chained
    def find_one(self, filters: dict, sort_criteria: List[tuple] = None) -> Union[dict, 'MongoDBModel']:
        return self._collection.find_one(filters, sort=sort_criteria, projection=self._projection)

    def post(self, payload: dict) -> Union[InsertOneResult, 'MongoDBModel']:
        record = self.on_pre_save(payload)
        query: InsertOneResult = self._collection.insert_one({**record, **({
                                                                               'created_at': datetime.now(),
                                                                               'updated_at': datetime.now()
                                                                           } if self.timestamp else {})})
        self.on_save({'_id': query.inserted_id, **record})
        return query

    @chained
    def put(self, pk: str, payload: dict) -> Union[dict, 'MongoDBModel']:
        record = self.on_pre_update(payload)
        old_record = MongoDBModel.get(self, pk).json()
        query = self._collection.find_one_and_update({'_id': ObjectId(pk)},
                                                     {'$set': {**record, **({
                                                                                'updated_at': datetime.now()
                                                                            } if self.timestamp else {})}},
                                                     projection=self._projection)

        self.on_update(old_record, record)
        return query

    @chained
    def patch(self, pk: str, payload: dict) -> Union[dict, 'MongoDBModel']:
        record = self.on_pre_partial_update(payload)
        old_record = MongoDBModel.get(self, pk).json()
        query = self._collection.find_one_and_update({'_id': ObjectId(pk)},
                                                     {'$push': record,
                                                      '$set':
                                                          {**({
                                                                  'updated_at': datetime.now()
                                                              } if self.timestamp else {})}
                                                      },
                                                     projection=self._projection)
        self.on_partial_update(record, old_record)
        return query

    @chained
    def put_patch(self, pk: str, put_record: dict, patch_record: dict) -> Union[dict, 'MongoDBModel']:
        return self._collection.find_one_and_update({'_id': ObjectId(pk)},
                                                    {'$set': {**put_record, **({
                                                                                   'updated_at': datetime.now()
                                                                               } if self.timestamp else {})},
                                                     '$push': patch_record},
                                                    projection=self._projection)

    def delete(self, pk: str) -> bool:
        self.on_delete(MongoDBModel.get(self, pk).json())
        return bool(self._collection.find_one_and_delete({'_id': ObjectId(pk)}, projection=self._projection))

    def count(self, filters: dict = None) -> int:
        return self._collection.count_documents(filters if filters else {})

    def distinct_values(self, key: str) -> list:
        return self._collection.distinct(key)

    # def mass_patch(self):
    #     return self._collection.update_many(
    #         {},
    #         [
    #             {
    #                 '$set': {
    #                     'created_at': {'$toDate': '$created_at'},
    #                     'updated_at': datetime.utcnow()
    #                 }
    #             }
    #         ]
    #     )
