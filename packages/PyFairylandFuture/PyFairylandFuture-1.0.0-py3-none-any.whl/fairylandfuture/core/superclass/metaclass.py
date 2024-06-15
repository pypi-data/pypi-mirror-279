# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-18 下午5:21:05 UTC+8
"""

import functools
from typing import Any


class SingletonMeta(type):
    """
    Singleton pattern metaclass
    """

    @functools.lru_cache(maxsize=0)
    def __call__(cls, *args: Any, **kwargs: Any):
        """
        Singleton pattern metaclass

        :param args: ...
        :type args: tuple
        :param kwargs: ...
        :type kwargs: dict
        :return: get instance
        :rtype: object
        """
        if not hasattr(cls, "__instance"):
            setattr(cls, "__instance", super().__call__(*args, **kwargs))
            return getattr(cls, "__instance")
        else:
            return getattr(cls, "__instance")
