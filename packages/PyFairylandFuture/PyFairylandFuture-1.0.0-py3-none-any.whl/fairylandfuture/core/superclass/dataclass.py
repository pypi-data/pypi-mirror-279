# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-04 上午10:38:31 UTC+8
"""

import json

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class BaseData:

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return json.dumps(self.__dict__)
