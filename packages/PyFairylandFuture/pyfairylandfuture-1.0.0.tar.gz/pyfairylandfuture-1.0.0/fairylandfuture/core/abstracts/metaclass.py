# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-10 10:58:14 UTC+8
"""

import abc
from typing import Dict


class SingletonABCMeta(abc.ABCMeta):
    """
    Singleton meta
    """

    _instances: Dict[type, object] = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances.update({cls: super().__call__(*args, **kwargs)})
        return cls._instances.get(cls)
