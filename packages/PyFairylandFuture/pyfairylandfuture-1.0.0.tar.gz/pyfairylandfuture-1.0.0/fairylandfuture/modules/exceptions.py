# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-10 11:40:48 UTC+8
"""


class ProgramError(Exception):

    def __init__(self, message: str = "Internal program error."):
        self.__prompt = f"{self.__class__.__name__}: {message}"

    def __str__(self) -> str:
        return self.__prompt


class ParameterError(ProgramError):

    def __init__(self, message: str = "Parameter error."):
        super().__init__(message)


class ParameterTypeError(ProgramError):

    def __init__(self, message: str = "Parameter type error."):
        super().__init__(message)


class ParameterValueError(ProgramError):

    def __init__(self, message: str = "Parameter value error."):
        super().__init__(message)


class FileReadError(ProgramError):

    def __init__(self, message: str = "File read error."):
        super().__init__(message=message)


class ConfigReadError(ProgramError):

    def __init__(self, message: str = "Config read error."):
        super().__init__(message=message)


class SQLExecutionError(ProgramError):

    def __init__(self, message: str = "SQL execution error."):
        super().__init__(message=message)
