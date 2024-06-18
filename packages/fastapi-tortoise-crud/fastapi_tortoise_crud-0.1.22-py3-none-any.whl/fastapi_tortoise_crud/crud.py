from typing import Union, Any, List, Callable
from fastapi import APIRouter, Depends
from tortoise.contrib.pydantic import PydanticModel
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate
from .model import BaseModel
from .response import BaseApiOut


class PreMixin:
    @classmethod
    async def pre_create(cls, item: PydanticModel) -> dict:
        return item.model_dump()

    @classmethod
    async def pre_create_all(cls, items: List[PydanticModel]):
        for item in items:
            yield await cls.pre_create(item)

    @classmethod
    async def pre_update(cls, item: PydanticModel, item_id: str) -> dict:
        return item.model_dump(exclude_unset=True)

    @classmethod
    async def pre_list(cls, item: PydanticModel) -> dict:
        """
        数据预处理：搜索字段
        :param item:
        :return:
        """
        data = {}
        for k, v in item.model_dump(exclude_unset=True).items():
            # 如果v有值或者为bool类型
            if v or isinstance(v, bool):
                # 如果v为字符串并且有值，则使用模糊搜索
                if isinstance(v, str):
                    data[f'{k}__icontains'] = v
                # 否则使用精确搜索
                else:
                    data[k] = v
        return data
        # return {f'{k}__icontains': v for k, v in item.model_dump(exclude_defaults=True).items() if v}


class ModelCrud(APIRouter, PreMixin):
    def __init__(self, model: Union[BaseModel, Any],
                 schema_list=None,
                 schema_create=None,
                 schema_read=None,
                 schema_update=None,
                 schema_delete=None,
                 schema_filters=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.schema_list = schema_list or model.schema_list()
        self.schema_read = schema_read or model.schema_read()
        self.schema_update = schema_update or model.schema_update()
        self.schema_create = schema_create or model.schema_create()
        self.schema_delete = schema_delete or model.schema_delete()
        self.schema_filters = schema_filters or model.schema_filters()

    @property
    def route_list(self) -> Callable:
        schema_filters = self.schema_filters

        async def route(filters: schema_filters, params: Params = Depends(), order_by: str = '-create_time'):
            filter_item = await self.pre_list(filters)
            queryset = self.model.filter(**filter_item)
            if order_by:
                queryset = queryset.order_by(*order_by.split(','))
            data = await paginate(queryset, params, True)
            return BaseApiOut(data=data)

        return route

    @property
    def route_read(self) -> Callable:
        async def route(item_id):
            data = await self.model.find_one(id=item_id)
            data = await self.schema_read.from_tortoise_orm(data)
            return BaseApiOut(data=data)

        return route

    @property
    def route_create(self) -> Callable:
        schema_create = self.schema_create

        async def route(item: schema_create):
            item = await self.pre_create(item)
            new_item = await self.model.create_one(item)
            return BaseApiOut(data=new_item)

        return route

    @property
    def route_create_all(self) -> Callable:
        schema_create = self.schema_create

        async def route(items: List[schema_create]):
            # items = self.pre_create_all(items)
            await self.model.bulk_create([self.model(**item) async for item in self.pre_create_all(items)],
                                         ignore_conflicts=False)
            return BaseApiOut(message='批量创建成功')

        return route

    @property
    def route_update(self) -> Callable:
        schema_update = self.schema_update

        async def route(item_id: str, item: schema_update):
            item = await self.pre_update(item, item_id=item_id)
            data = await self.model.update_one(item_id, item)
            return BaseApiOut(data=data)

        return route

    @property
    def route_delete(self) -> Callable:
        async def route(item_ids: str):
            ids = item_ids.split(',')
            data = await self.model.delete_many(ids)
            return BaseApiOut(data=data)

        return route

    @property
    def route_delete_all(self) -> Callable:
        async def route():
            await self.model.all().delete()
            return BaseApiOut(message='删除所有数据成功')

        return route

    def register_crud(self,
                      depends_list: List[Depends] = None,
                      depends_create: List[Depends] = None,
                      depends_update: List[Depends] = None,
                      depends_delete: List[Depends] = None,
                      ):
        model_name = self.model.__name__.lower()

        self.add_api_route(
            '/list',
            self.route_list,
            methods=['POST'],
            response_model=BaseApiOut[Page[self.schema_list]],
            name=f'{model_name}Read',
            summary=f'{model_name} List',
            dependencies=depends_list
        )
        self.add_api_route(
            '/read/{item_id}',
            self.route_read,
            methods=['GET'],
            response_model=BaseApiOut[self.schema_read],
            name=f'{model_name}Read',
            summary=f'{model_name} Read',
            dependencies=depends_list
        )

        self.add_api_route(
            '/create',
            self.route_create,
            methods=['POST'],
            response_model=BaseApiOut,
            name=f'{model_name}Create',
            summary=f'{model_name} Create',
            dependencies=depends_create
        )

        self.add_api_route(
            '/create/all',
            self.route_create_all,
            methods=['POST'],
            response_model=BaseApiOut,
            name=f'{model_name}Create',
            summary=f'{model_name} CreateAll',
            dependencies=depends_create
        )

        self.add_api_route(
            '/{item_id}',
            self.route_update,
            methods=['PUT'],
            response_model=BaseApiOut,
            name=f'{model_name}Update',
            summary=f'{model_name} Update',
            dependencies=depends_update
        )

        self.add_api_route(
            '/{item_ids}',
            self.route_delete,
            methods=['DELETE'],
            response_model=BaseApiOut,
            description='删除1条或多条数据example：1,2',
            name=f'{model_name}Delete',
            summary=f'{model_name} Delete',
            dependencies=depends_delete
        )
        self.add_api_route(
            '/delete/all',
            self.route_delete_all,
            methods=['DELETE'],
            response_model=BaseApiOut,
            description='删除所有数据',
            name=f'{model_name}Delete',
            summary=f'{model_name}DeleteAll',
            dependencies=depends_delete
        )
        return self


__all__ = [
    'ModelCrud'
]
