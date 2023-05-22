from typing import Any, Sequence, Tuple
from aiomysql.cursors import Cursor



class BaseRepository:
    def __init__(self, cur: Cursor) -> None:
        self._cur = cur
        
    @property
    def connection(self) -> Cursor:
        self._cur
        
    async def execute(self, query: str, *query_params: Any) -> int:
        await self._cur.execute(query, *query_params)
        created_id = self._cur.lastrowid
        return created_id
        
    async def execute_many(self, query: str, *queryparams: Sequence[Tuple[Any, ...]]) -> None:
        await self._cur.executemany(query, *queryparams)
        
    async def fetch_one(self, query: str, *queryparams: Any) -> Any:
        await self._cur.execute(query, *queryparams)
        return await self._cur.fetchone()
    
    async def fetch_all(self, query: str, *queryparams: Any) -> Any:
        await self._cur.execute(query, *queryparams)
        return await self._cur.fetchall()