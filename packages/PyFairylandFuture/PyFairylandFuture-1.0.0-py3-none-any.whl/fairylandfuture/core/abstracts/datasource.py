# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-12 22:23:51 UTC+8
"""

from typing import List

import abc

from fairylandfuture.models.dataclass.datasource import ExecuteParams, InsertManyParams


class AbstractDataSource(abc.ABC):

    @abc.abstractmethod
    def execute(self, params: ExecuteParams) -> bool: ...

    def insert(self, params: ExecuteParams) -> bool:
        return self.execute(params)

    def delete(self, params: ExecuteParams) -> bool:
        return self.execute(params)

    def update(self, params: ExecuteParams) -> bool:
        return self.execute(params)

    @abc.abstractmethod
    def select(self, params: ExecuteParams): ...

    @abc.abstractmethod
    def multiple(self, params: List[ExecuteParams]) -> bool: ...

    @abc.abstractmethod
    def insertmany(self, params: InsertManyParams) -> bool: ...
