# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-12 23:11:45 UTC+8
"""

from typing import Union, Dict, List, Any, Iterable

import pymysql
from pymysql.cursors import DictCursor

from fairylandfuture.core.abstracts.datasource import AbstractDataSource
from fairylandfuture.models.dataclass.datasource import ExecuteParams, InsertManyParams


class MySQLDataSource(AbstractDataSource):

    def __init__(self, host, port, user, password, database):
        self._connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database, cursorclass=DictCursor)
        self._cursor = self._connection.cursor()

    def execute(self, params: ExecuteParams):
        try:
            self._cursor.execute(params.expression, params.params)
            self._connection.commit()
            return True
        except Exception as err:
            self._connection.rollback()
            raise err

    def select(self, params: ExecuteParams) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        try:
            self._cursor.execute(params.expression, params.params)
            result = self._cursor.fetchall()
            if len(result) == 1:
                return result.__getitem__(0)  # type: Dict[str ,Any]
            return result  # type: List[Dict[str, Any]]
        except Exception as err:
            raise err

    def multiple(self, params: Iterable[ExecuteParams]) -> bool:
        try:
            for param in params:
                self._cursor.execute(param.expression, param.params)
            self._connection.commit()
            return True
        except Exception as err:
            self._connection.rollback()
            raise err

    def insertmany(self, params: InsertManyParams) -> bool:
        try:
            self._cursor.executemany(params.expression, params.params)
            self._connection.commit()
        except Exception as err:
            self._connection.rollback()
            raise err

    def __del__(self):
        self._cursor.close()
        self._connection.close()
