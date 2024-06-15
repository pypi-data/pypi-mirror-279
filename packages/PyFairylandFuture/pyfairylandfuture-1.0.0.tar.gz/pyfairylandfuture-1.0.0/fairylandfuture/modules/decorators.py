# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-10 10:20:53 UTC+8
"""

import time

from functools import wraps
from typing import Optional, Type, TypeVar, Generic

from fairylandfuture.core.superclass.decorators import BaseDecorator, BaseParamsDecorator

_T = TypeVar("_T")


class SingletonDecorator(Generic[_T]):
    """
    Singleton decorator.

    Usage:
        >>> @SingletonDecorator
        >>> class MyClass:
        >>>     pass
        >>>
        >>> obj1 = MyClass()
        >>> obj2 = MyClass()
        >>> obj1 is obj2
        True
    """

    _instances = {}

    def __init__(self, cls: Type[_T]):
        self._cls = cls

    def __call__(self, *args, **kwargs) -> _T:
        if self._cls not in self._instances:
            self._instances[self._cls] = self._cls(*args, **kwargs)
        return self._instances[self._cls]

    def __instancecheck__(self, instance: object) -> bool:
        return isinstance(instance, self._cls)


class TimingDecorator(BaseDecorator):
    """
    Timing decorator.

    Usage:
        >>> @TimingDecorator
        >>> def my_func():
        >>>     pass
        >>>
        >>> my_func()
        Running for 00:00:00.000
    """

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        results = super().__call__(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        hour, minute, second = self._calculate_time_parts(elapsed_time)
        elapsed_str = f"Running for {hour:02d}:{minute:02d}:{second:06.3f}"
        self.output(elapsed_str)
        return results

    @staticmethod
    def _calculate_time_parts(elapsed_time):
        if elapsed_time < 60:
            return 0, 0, elapsed_time
        elif elapsed_time < 3600:
            return 0, int(elapsed_time / 60), elapsed_time % 60
        else:
            hour = int(elapsed_time / 3600)
            return hour, int((elapsed_time - (hour * 3600)) / 60), elapsed_time % 60

    def output(self, msg: str) -> None:
        """
        Output message.
            rewrote this method to print message to console instead of logging.

        :param msg: Message to output.
        :type msg: str
        :return: ...
        :rtype: ...
        """
        print(msg)


class ActionDecorator(BaseParamsDecorator):
    """
    Action decorator.

    Usage:
        >>> @ActionDecorator(action="my_action")
        >>> def my_func():
        >>>     pass
        >>>
        >>> my_func()
        Running: my_action.
        Success: my_action.
    """

    def __init__(self, action=None):
        super().__init__()
        self.action = action

    def __call__(self, *args, **kwargs):
        if args and len(args) == 1 and callable(args.__getitem__(0)):
            self.func: Type = args.__getitem__(0)
        action_name = self.action if self.action else self.func.__name__

        @wraps(self.func)
        def wrapper(*args, **kwargs):
            try:
                self.output(msg=f"Running: {action_name}.")
                result = self.func(*args, **kwargs)
                self.output(msg=f"Success: {action_name}.")
                return result
            except Exception as err:
                self.output(msg=f"Failure: {action_name}.")
                raise err

        return wrapper

    def output(self, msg: str) -> None:
        """
        Output message.
            rewrote this method to print message to console instead of logging.

        :param msg: Message to output.
        :type msg: str
        :return: ...
        :rtype: ...
        """
        print(msg)


class TryCatchDecorator(BaseDecorator):
    """
    Try-catch decorator.

    Usage:
        >>> @TryCatchDecorator
        >>> def my_func():
        >>>     pass
        >>>
        >>> my_func()
    """

    def __call__(self, *args, **kwargs):
        try:
            results = self.func(*args, **kwargs)
            return results
        except Exception as err:
            raise err


class TipsDecorator(BaseParamsDecorator):
    """
    Tips decorator.

    Usage:
        >>> @TipsDecorator(tips="This is a tips.")
        >>> def my_func():
        >>>     pass
        >>>
        >>> my_func()
        Running tips: my_func.
    """

    def __init__(self, tips: Optional[str] = None):
        super().__init__()
        self.tips = tips

    def __call__(self, *args, **kwargs):
        if args and len(args) == 1 and callable(args.__getitem__(0)):
            self.func: Type = args.__getitem__(0)

        @wraps(self.func)
        def wrapper(*args, **kwargs):
            try:
                self.output(f"Running tips: {self.tips if self.tips else self.func.__name__}")
                results = self.func(*args, **kwargs)
                return results
            except Exception as err:
                raise err

        return wrapper

    def output(self, msg: str) -> None:
        """
        Output message.
            rewrote this method to print message to console instead of logging.

        :param msg: Message to output.
        :type msg: str
        :return: ...
        :rtype: ...
        """
        print(msg)
