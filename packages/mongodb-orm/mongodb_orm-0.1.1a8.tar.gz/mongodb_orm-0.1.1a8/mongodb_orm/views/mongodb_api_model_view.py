import json
from pymongo.results import InsertOneResult
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from ..interfaces.mongodb_model import MongoDBModel
from ..utils.helpers import Helper


class MongoDBAPIModelView(MongoDBModel, ViewSet):

    def list(self: MongoDBModel, request, *args, **kwargs) -> Response:
        MongoDBModel.set_tenant(self, tenant_name=request.headers.get('database', 'public'))
        page: int = request.query_params.get('page', 1)
        per_page: int = request.query_params.get('per_page', 5)
        order_by: str = request.query_params.get('order_by', None)
        order_mode: int = request.query_params.get('order_mode', 1)
        filters: str = request.query_params.get('filters', {})
        sort_by = None
        if order_by:
            sort_by = (order_by, int(order_mode))
        query = MongoDBModel.get_all(self, filters=Helper.standard_record(json.loads(filters)) if filters else None, page=int(page),
                                     per_page=int(per_page),
                                     sort_by=sort_by)
        return Response({'success': True, 'result': query.json()})

    def retrieve(self, request, *args, **kwargs) -> Response:
        MongoDBModel.set_tenant(self, tenant_name=request.headers.get('database', 'public'))
        try:
            result = MongoDBModel.get(self, pk=str(kwargs.get('pk')))
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        return Response({'success': True, 'result': result.json()})

    @action(methods=['get'], detail=False)
    def get_record_by_filters(self, request, *args, **kwargs) -> Response:
        MongoDBModel.set_tenant(self, tenant_name=request.headers.get('database', 'public'))
        filters: str = request.query_params.get('filters', None)
        if not filters:
            return Response({'success': False, 'error': 'you need to provide at least one filter'})
        try:
            result = MongoDBModel.find_one(self, filters=json.loads(filters))
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        return Response({'success': True, 'result': result.json()})

    def create(self, request, *args, **kwargs) -> Response:
        MongoDBModel.set_tenant(self, tenant_name=request.headers.get('database', 'public'))
        try:
            new_record: InsertOneResult = MongoDBModel.post(self, Helper.standard_record(request.data))
            retrieve_record: dict = MongoDBModel.get(self, pk=str(new_record.inserted_id)).json()
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        return Response({'success': True, 'record': retrieve_record})

    def update(self, request, *args, **kwargs) -> Response:
        MongoDBModel.set_tenant(self, tenant_name=request.headers.get('database', 'public'))
        try:
            MongoDBModel.put(self, pk=str(kwargs.get('pk')), payload=Helper.standard_record(request.data))
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        return Response({'success': True})

    def partial_update(self, request, *args, **kwargs) -> Response:
        MongoDBModel.set_tenant(self, tenant_name=request.headers.get('database', 'public'))
        try:
            MongoDBModel.patch(self, pk=str(kwargs.get('pk')), payload=Helper.standard_record(request.data))
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        return Response({'success': True})

    def destroy(self, request, *args, **kwargs) -> Response:
        MongoDBModel.set_tenant(self, tenant_name=request.headers.get('database', 'public'))
        try:
            result = MongoDBModel.delete(self, pk=str(kwargs.get('pk')))
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        return Response({'success': result})
