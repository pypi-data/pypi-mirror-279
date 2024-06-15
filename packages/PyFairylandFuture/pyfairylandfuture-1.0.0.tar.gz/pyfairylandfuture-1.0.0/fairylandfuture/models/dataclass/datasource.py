# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-18 下午6:44:40 UTC+8
"""

from typing import Tuple, Optional, Any, Union, List, Dict

from dataclasses import dataclass, field


@dataclass
class ExecuteParams:
    """
    Execcute Query parameters for a data source.

    Attrs:
        expression: The SQL expression to execute.
        params: The parameters to substitute into the expression.
    Usage:
        >>> from fairylandfuture.models.dataclass.datasource import ExecuteParams
        >>> ExecuteParams(expression="select * from table where id = %s", params=[1])
        QueryParams(expression='select * from table where id = %s', params=[1])
    Note:
        The `params` attribute can be a list, tuple, or dictionary. If it is a list or tuple,
        the values will be substituted in the order they appear in the list or tuple. If it is a dictionary,
        the values will be substituted by their keys.
    """

    expression: str
    params: Optional[Union[List[Any], Tuple[Any, ...], Dict[str, Any]]] = field(default=None)


@dataclass
class InsertManyParams:
    """
    Multiple Execute Query parameters for a data source.

    Attrs:
        expression: The SQL expression to execute.
        params: The parameters to substitute into the expression.
    Usage:
        >>> from fairylandfuture.models.dataclass.datasource import InsertManyParams
        >>> parasm = [
        >>>     ("郝淑慧", 18),
        >>>     ("李雪琴", 19)
        >>> ]
        >>> InsertManyParams(expression="insert into table (name, age) values (%s, %s)", params=parasm)
        MultipleParams(expression='insert into table (name, age) values (%s, %s)', params=[('郝淑慧', 18), ("李雪琴", 19)])
    """

    expression: str
    params: Union[List[Union[List[Any], Tuple[Any, ...], Dict[str, Any]]], Tuple[Union[List[Any], Tuple[Any, ...], Dict[str, Any]], ...]]
