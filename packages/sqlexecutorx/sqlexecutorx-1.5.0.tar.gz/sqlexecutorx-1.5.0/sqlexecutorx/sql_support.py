from functools import lru_cache
from .constant import CACHE_SIZE


@lru_cache(maxsize=CACHE_SIZE)
def require_limit(sql: str):
    lower_sql = sql.lower()
    if 'limit' not in lower_sql:
        return True
    idx = lower_sql.rindex('limit')
    if idx > 0 and ')' in lower_sql[idx:]:
        return True
    return False


@lru_cache(maxsize=CACHE_SIZE)
def limit_one_sql(sql: str, placeholder: str = '?'):
    return f'{sql} LIMIT {placeholder}'

