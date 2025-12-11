import asyncpg
from typing import Optional, List, Dict, Any
from collections import deque
from imports import *

class Database:

    def __init__(self, dsn: str = None, log_size: int = 50, **kwargs):
        """
        log_size: تعداد آخرین لاگ‌ها که نگه داشته می‌شوند
        """
        self.pool: Optional[asyncpg.Pool] = None
        self.log = deque(maxlen=log_size)
        self.dsn = dsn or f"postgresql://{kwargs['user']}:{kwargs['password']}@{kwargs['host']}:{kwargs['port']}/{kwargs['database']}"
        self.pool_kwargs = {
            "min_size": kwargs.get("min_size", 5),
            "max_size": kwargs.get("max_size", 20),
            "command_timeout": kwargs.get("command_timeout", 60),
            "timeout": kwargs.get("timeout", 30),
        }

    # ----------------------
    # اتصال و بستن Pool
    # ----------------------
    async def connect(self) -> None:
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, **self.pool_kwargs)

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            self.pool = None

    # ----------------------
    # Logging helper
    # ----------------------
    def _log(self, message: str):
        self.log.append(message)  # همیشه فقط آخرین‌ها نگه داشته می‌شوند

    # ----------------------
    # CRUD Methods
    # ----------------------
    async def insert(self, table: str, data: dict) -> Dict[str, Any]:
        columns = ', '.join(f'"{col}"' for col in data.keys())
        placeholders = ', '.join(f"${i+1}" for i in range(len(data)))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *data.values())
            self._log(f"INSERT {table}: {data}")
            return dict(row)

    # فقط بخش متد select رو جایگزین کن
async def select(
    self,
    table: str,
    columns: Optional[List[str]] = None,
    where: Optional[Dict[str, Any]] = None,
    raw_where: Optional[str] = None,
    raw_values: Optional[List[Any]] = None
) -> List[Dict[str, Any]]:
    cols = ', '.join(f'"{col}"' for col in columns) if columns else '*'
    values: List[Any] = []
    query = f"SELECT {cols} FROM {table}"

    if where or raw_where:
        query += " WHERE "
        conditions = []
        if where:
            for i, k in enumerate(where.keys()):
                conditions.append(f'"{k}" = ${len(values) + 1}')
                values.append(where[k])
        if raw_where:
            conditions.append(raw_where)
            if raw_values:
                values.extend(raw_values)
        query += " AND ".join(conditions) if len(conditions) > 1 else conditions[0]

    async with self.pool.acquire() as conn:
        rows = await conn.fetch(query, *values)
        return [dict(row) for row in rows]
    
    
    async def update(self, table: str, data: dict, where: dict) -> Optional[Dict[str, Any]]:
        set_keys = list(data.keys())
        where_keys = list(where.keys())
        set_clause = ', '.join(f'"{k}" = ${i+1}' for i, k in enumerate(set_keys))
        where_clause = ' AND '.join(f'"{k}" = ${i+len(set_keys)+1}' for i, k in enumerate(where_keys))
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause} RETURNING *"
        values = list(data.values()) + list(where.values())
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *values)
            self._log(f"UPDATE {table} SET {data} WHERE {where}")
            return dict(row) if row else None

    async def delete(self, table: str, where: dict) -> Optional[Dict[str, Any]]:
        where_keys = list(where.keys())
        where_clause = ' AND '.join(f'"{k}" = ${i+1}' for i, k in enumerate(where_keys))
        query = f"DELETE FROM {table} WHERE {where_clause} RETURNING *"
        values = list(where.values())
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *values)
            self._log(f"DELETE {table} WHERE {where}")
            return dict(row) if row else None

    async def exists(self, table: str, where: dict) -> bool:
        where_keys = list(where.keys())
        where_clause = ' AND '.join(f'"{k}" = ${i+1}' for i, k in enumerate(where_keys))
        query = f"SELECT 1 FROM {table} WHERE {where_clause} LIMIT 1"
        values = list(where.values())
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *values)
            self._log(f"EXISTS {table} WHERE {where} -> {row is not None}")
            return row is not None
        
db_connect = {
    "user": os.getenv("USERDB"),
    "password": os.getenv("PDB"),
    "host": os.getenv("HOSTDB"),
    "port": os.getenv("PORTDB"),
    "database": os.getenv("NAMEDB"),
}

db = Database(**db_connect)
