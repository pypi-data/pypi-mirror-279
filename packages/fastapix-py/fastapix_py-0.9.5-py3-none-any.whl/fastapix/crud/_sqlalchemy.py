# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : _sqlalchemy.py.py
# @Time     : 2023/10/11 16:11
import copy
from typing import List, Dict, Any, TypeVar, Optional, Type, Tuple, Union, Mapping, Sequence

from fastapi.requests import Request
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import func, Result, Executable, Dialect
from sqlalchemy.engine import Row
from sqlalchemy.orm import object_session, InstrumentedAttribute
from sqlalchemy.sql.elements import Label
from sqlmodel import SQLModel, select, Session

from fastapix.common.pydantic import model_validate, model_dump
from fastapix.crud._models import SQLModelParser
from fastapix.crud._router import CrudRouterManager
from fastapix.crud._selecter import get_modelfield_by_alias, Selector, Paginator
from fastapix.crud.database import SqlalchemyDatabase, EngineDatabase

TableModel = TypeVar('TableModel', bound=SQLModel)

EMPTY_LIST: list = []


class SQLAlchemyCrud(SQLModelParser):

    def __init__(self, model: Type[TableModel], engine: SqlalchemyDatabase,
                 create_exclude_fields: List[Union[str, InstrumentedAttribute, Label]] = None,
                 read_extra_fields: List[Union[str, InstrumentedAttribute, Label]] = None,
                 update_exclude_fields: List[Union[str, InstrumentedAttribute, Label]] = None
                 ):
        super().__init__(
            model,
            read_extra_fields=read_extra_fields,
            create_extra_fields=create_exclude_fields,
            update_extra_fields=update_exclude_fields
        )
        assert engine, "engine is None"
        self.db = EngineDatabase(engine)
        self.dialect: Dialect = self.db.engine.dialect

        self.name = model.__name__
        logger.info(f"Building table {{{self.name}}} RESTful API...")
        self.CreateModel: Type[BaseModel] = self.create_schema_create()
        self.ReadModel: Type[BaseModel] = self.create_schema_read()
        self.UpdateModel: Type[BaseModel] = self.create_schema_update()

    async def on_before_create(
            self, objects: List[BaseModel], request: Optional[Request] = None
    ) -> None:
        return  # pragma: no cover

    async def on_after_create(
            self, objects: List[BaseModel], request: Optional[Request] = None
    ) -> None:
        return  # pragma: no cover

    async def on_after_read(
            self, objects: List[BaseModel], request: Optional[Request] = None
    ) -> None:
        return  # pragma: no cover

    async def on_before_update(
            self,
            primary_key: List[Any],
            new_obj: BaseModel,
            request: Optional[Request] = None,
    ) -> None:
        return  # pragma: no cover

    async def on_after_update(
            self,
            objects: List[BaseModel],
            request: Optional[Request] = None,
    ) -> None:
        return  # pragma: no cover

    async def on_before_delete(
            self, primary_key: List[Any], request: Optional[Request] = None
    ) -> None:
        return  # pragma: no cover

    async def on_after_delete(
            self, objects: List[BaseModel], request: Optional[Request] = None
    ) -> None:
        return  # pragma: no cover

    def _fetch_item_scalars(self, session: Session, query=None) -> Sequence[TableModel]:
        sel = select(self.Model)
        if query is not None:
            sel = sel.filter(query)
        return session.scalars(sel).all()

    def pyobj_to_table(self, item: BaseModel) -> TableModel:
        return self.Model(**model_dump(item))

    def table_to_pyobj(self, obj: Row) -> BaseModel:
        return model_validate(self.ReadModel, obj, from_attributes=True)

    def _update_item(self, obj: TableModel, values: Dict[str, Any]):
        if isinstance(obj, dict):
            for k, v in values.items():
                if isinstance(v, dict):
                    sub = getattr(obj, k)
                    if sub:
                        v = self._update_item(sub, v)
                obj[k] = v
        else:
            for k, v in values.items():
                field = get_modelfield_by_alias(self.Model, k)
                if not field and not hasattr(obj, k):
                    continue
                name = field.name if field else k
                if isinstance(v, dict):
                    sub = getattr(obj, name)
                    if sub:
                        v = self._update_item(copy.deepcopy(sub), v)
                setattr(obj, name, v)
        return obj

    def _delete_item(self, obj: TableModel) -> None:
        object_session(obj).delete(obj)

    def _create_items(self, session: Session, items: List[BaseModel]) -> List[BaseModel]:
        if not items:
            return []
        objs = [self.pyobj_to_table(item) for item in items]
        session.add_all(objs)
        session.flush()
        results = [self.table_to_pyobj(obj) for obj in objs]
        return results

    async def create_items(
            self, items: List[BaseModel], request: Request = None,
    ) -> List[BaseModel]:
        await self.on_before_create(items, request=request)
        results = await self.db.async_run(self._create_items, items)
        await self.on_after_create(results, request=request)
        return results

    def _read_items(self, session: Session, query=None) -> List[BaseModel]:
        items = self._fetch_item_scalars(session, query)
        return [self.table_to_pyobj(obj) for obj in items]

    async def read_item_by_primary_key(self, primary_key: Any, request: Request = None) -> BaseModel:
        query = self.pk == primary_key
        items = await self.db.async_run(self._read_items, query)
        await self.on_after_read(items, request)
        return items[0] if len(items) == 1 else None

    async def read_items(
            self,
            selector: Selector = None,
            paginator: Paginator = None,
            request: Request = None
    ) -> Tuple[List[BaseModel], int]:
        sel = self.get_select()
        if selector:
            selector = selector.calc_filter_clause(self.dialect.name)
            if selector:
                sel = sel.filter(*selector)
        total = -1
        if paginator:
            if paginator.show_total:
                total = await self.db.async_scalar(
                    select(func.count("*")).select_from(sel.with_only_columns(self.pk).subquery())
                )

            order_by = paginator.calc_ordering()
            if order_by:
                sel = sel.order_by(*order_by)
            if paginator.page_size and paginator.page_size > 0:
                sel = sel.limit(paginator.page_size).offset((paginator.page - 1) * paginator.page_size)

        results = await self.db.async_execute(sel)
        results = results.all()
        results = [self.table_to_pyobj(r) for r in results]
        await self.on_after_read(results, request)
        return results, total

    def _update_items(
            self, session: Session, primary_key: List[Any], values: Dict[str, Any], query=None
    ) -> Sequence[BaseModel]:
        query = query or self.pk.in_(primary_key)
        objs = self._fetch_item_scalars(session, query)
        results = []
        for obj in objs:
            self._update_item(obj, values)
            results.append(self.table_to_pyobj(obj))
        return results

    async def update_items(
            self, primary_key: List[Any], item: BaseModel,
            request: Request = None
    ) -> List[BaseModel]:
        await self.on_before_update(primary_key, item)
        results = await self.db.async_run(
            self._update_items, primary_key, model_dump(item, exclude_unset=True), None
        )
        await self.on_after_update(results, request)
        return results

    def _delete_items(self, session: Session, primary_key: List[Any]) -> Sequence[BaseModel]:
        query = self.pk.in_(primary_key)
        objs = self._fetch_item_scalars(session, query)
        results = []
        for obj in objs:
            self._delete_item(obj)
            results.append(self.table_to_pyobj(obj))
        return results

    async def delete_items(
            self, primary_key: List[Any],
            request: Request = None
    ) -> List[BaseModel]:
        await self.on_before_delete(primary_key)
        results = await self.db.async_run(self._delete_items, primary_key)
        await self.on_after_delete(results, request)
        return results

    async def async_execute(
        self,
        statement: Executable,
        params: Optional[Union[Mapping[Any, Any], List[Mapping[Any, Any]]]] = None,
        execution_options: Optional[Mapping[Any, Any]] = None,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> Result:
        return await self.db.async_execute(
            statement=statement, params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments, **kwargs
        )

    def router_manager(self) -> CrudRouterManager:
        return CrudRouterManager(self)
