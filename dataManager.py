# database.py
import asyncpg
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, dsn: str = None, **kwargs):
        self.pool: Optional[asyncpg.Pool] = None
        self.dsn = dsn or f"postgresql://{kwargs['user']}:{kwargs['password']}@{kwargs['host']}:{kwargs['port']}/{kwargs['database']}"
        self.pool_kwargs = {
            "min_size": kwargs.get("min_size", 5),
            "max_size": kwargs.get("max_size", 20),
            "command_timeout": 60,
            "timeout": 30,
        }

    async def connect(self) -> None:
        """فقط یک بار موقع استارت اپ صدا بزن"""
        if self.pool is None:
            try:
                self.pool = await asyncpg.create_pool(**self.pool_kwargs)
                logger.info("Database pool created successfully")
            except Exception as e:
                logger.error(f"Failed to create database pool: {e}")
                raise

    async def close(self) -> None:
        """موقع shutdown اپ صدا بزن"""
        if self.pool:
            await self.pool.close()
            logger.info("Database pool closed")

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]

    async def fetchrow(self, query: str, *args) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None

    async def execute(self, query: str, *args) -> str:
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    # مثال‌های راحت‌تر برای استفاده روزمره
    async def insert(self, table: str, data: dict) -> Dict[str, Any]:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(f"${i+1}" for i in range(len(data)))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        return await self.fetchrow(query, *data.values())

    async def update(self, table: str, data: dict, where: str, *where_args) -> Optional[Dict]:
        set_clause = ', '.join(f"{k} = ${i+1}" for i, k in enumerate(data.keys()))
        query = f"UPDATE {table} SET {set_clause} WHERE {where} RETURNING *"
        return await self.fetchrow(query, *data.values(), *where_args)

    async def delete(self, table: str, where: str, *args) -> Optional[Dict]:
        query = f"DELETE FROM {table} WHERE {where} RETURNING *"
        return await self.fetchrow(query, *args)