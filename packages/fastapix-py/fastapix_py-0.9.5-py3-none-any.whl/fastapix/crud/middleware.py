# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : middleware.py
# @Time     : 2024/5/14 下午4:15
# @Desc     :
from contextlib import AsyncExitStack

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from fastapix.crud.database import Database, AsyncDatabase, SqlalchemyDatabase


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            db: SqlalchemyDatabase,
    ):
        super().__init__(app)

        if isinstance(db, (Database, AsyncDatabase)):
            self.db = db
        if isinstance(db, Engine):
            self.db = Database(db)
        if isinstance(db, AsyncEngine):
            self.db = AsyncDatabase(db)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        scope = request.scope
        if not scope.get(f"__fastapix_database__:{id(self.db)}", False):
            exception = None
            async with AsyncExitStack() as async_stack:
                await async_stack.enter_async_context(self.db(scope=id(scope)))
                scope[f"__fastapix_database__:{id(self.db)}"] = self.db
                try:
                    response = await call_next(request)
                except Exception as e:
                    exception = e
                    await self.db.session.rollback()

            if exception:
                raise exception
        return response
