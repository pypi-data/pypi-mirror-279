# -*- coding: utf-8 -*-
"""
### Methods:
    - `get_base`
    - `get_model_by_tablename`
    - `persist_enums`
    - `persist_tables`
"""

from ._get_base import basemodel
from ._async_get import async_get
from ._get_many import get_many
from ._batch_list import batch_list

__all__ = [
    'async_get',
    'basemodel',
    'get_many',
    'batch_list'
]
