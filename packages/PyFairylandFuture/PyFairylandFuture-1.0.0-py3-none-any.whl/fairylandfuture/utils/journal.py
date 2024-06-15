# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-12 14:44:33 UTC+8
"""

from typing import Optional

import os.path
import sys

from loguru import logger
from importlib.resources import read_text

from fairylandfuture.constants.enums import EncodingEnum, LogLevelEnum
from fairylandfuture.constants.typed import TypeLogLevel
from fairylandfuture.core.superclass.metaclass import SingletonMeta


class Journal(metaclass=SingletonMeta):
    """
    A logging utility implemented as a singleton to ensure that only one instance
    handles logging across the application.

    :param path: Path to directory where log files are stored.
    :type path: str
    :param name: Name of the log file.
    :type name: str
    :param debug: Flag to set logging level to debug.
    :type debug: bool
    :param rotation: Log rotation size or time.
    :type rotation: str
    :param retention: Time period to retain old log files.
    :type retention: str
    :param format: Log message format.
    :type format: str or None
    :param compression: Compression format for rotated logs.
    :type compression: str
    :param encoding: Encoding for the log files.
    :type encoding: str
    :param level: Logging level for the file handler.
    :type level: TypeLogLevel
    :param enqueue: Flag to enable message queuing for logs.
    :type enqueue: bool
    :param colorize: Flag to enable log message colorization.
    :type colorize: bool
    :param backtrace: Include backtrace in log, useful for debugging.
    :type backtrace: bool
    :param diagnose: Include diagnostic info in logs.
    :type diagnose: bool
    :param serialize: Serialize log messages to JSON format.
    :type serialize: bool
    :param console: Flag to enable logging to console.
    :type console: bool
    :param console_level: Logging level for the console handler.
    :type console_level: TypeLogLevel
    :param console_format: Log message format for console.
    :type console_format: str or None
    :param console_colorize: Flag to enable log message colorization on console.
    :type console_colorize: bool
    :param console_enqueue: Flag to enable message queuing for console logs.
    :type console_enqueue: bool

    Usage::

        # Create a journal instance
        journal = Journal()

        # Log messages
        journal.info("This is an info message")
        journal.error("This is an error message")

    Note: This class uses `loguru` library for logging.
    The metaclass `SingletonMeta` ensures a single instance is used.
    """

    # ... rest of the class remains unchanged ...
    def __init__(
        self,
        path: str = "logs",
        name: str = "service.log",
        debug: bool = False,
        rotation: str = "20 MB",
        retention: str = "180 days",
        format: Optional[str] = None,
        compression: str = "gz",
        encoding: str = EncodingEnum.UTF_8.value,
        level: TypeLogLevel = LogLevelEnum.INFO.value,
        enqueue: bool = True,
        colorize: bool = False,
        backtrace: bool = False,
        diagnose: bool = True,
        serialize: bool = False,
        console: bool = True,
        console_level: TypeLogLevel = LogLevelEnum.TRACE.value,
        console_format: Optional[str] = None,
        console_colorize: bool = True,
        console_enqueue: bool = True,
    ):
        """
        Constructs all the necessary attributes for the Journal object.
        Initializes file and console loggers with specified configurations.
        """
        self.__path = path
        self.__name = name
        self.__debug = debug
        self.__rotation = rotation
        self.__retention = retention
        self.__format = format
        self.__compression = compression
        self.__level = level
        self.__encoding = encoding
        self.__enqueue = enqueue
        self.__colorize = colorize
        self.__backtrace = backtrace
        self.__diagnose = diagnose
        self.__serialize = serialize
        self.__console = console
        self.__console_level = console_level
        self.__console_format = console_format
        self.__console_colorize = console_colorize
        self.__console_enqueue = console_enqueue

        self.__logo = self.load_logo()

        self.__name, extension = os.path.splitext(self.__name)

        if self.__debug:
            self.__name += f".debug{extension if extension else '.log'}"
            self.__level = LogLevelEnum.DEBUG.value

        if not self.__format:
            self.__format = "[{time:YYYY-MM-DD HH:mm:ss} | Process ID: {process:<8} | Thread ID: {thread:<8} | {level:<8}]: {message}"

        # Fixed: Remove the default console output.
        logger.remove()

        logger.add(
            sink=os.path.join(self.__path, self.__name),
            rotation=self.__rotation,
            retention=self.__retention,
            format=self.__format,
            compression=self.__compression,
            encoding=self.__encoding,
            level=self.__level,
            enqueue=self.__enqueue,
            colorize=self.__colorize,
            backtrace=self.__backtrace,
            diagnose=self.__diagnose,
        )

        self.__write_logo(os.path.join(self.__path, self.__name))

        if self.__serialize:
            __serialize_name = f"{self.__name}.serialize{extension if extension else '.log'}"
            logger.add(
                sink=os.path.join(self.__path, __serialize_name),
                rotation=self.__rotation,
                retention=self.__retention,
                format=self.__format,
                compression=self.__compression,
                encoding=self.__encoding,
                level=self.__level,
                enqueue=self.__enqueue,
                colorize=self.__colorize,
                backtrace=self.__backtrace,
                diagnose=self.__diagnose,
                serialize=self.__serialize,
            )
            self.__write_logo(os.path.join(self.__path, self.__name))

        if self.__console:
            if not self.__console_format:
                self.__console_format = (
                    "<level>" "[{time:YYYY-MM-DD HH:mm:ss} | Process ID: {process:<8} | Thread ID: {thread:<8} | {level:<8}]: {message}" "</level>"
                )

            logger.add(
                sink=sys.stdout,
                format=self.__console_format,
                level=self.__console_level,
                colorize=self.__console_colorize,
                enqueue=self.__console_enqueue,
            )

            print(self.__logo)

    @staticmethod
    def load_logo():
        logo_text = read_text("fairylandfuture.conf", "logo")

        return logo_text

    def __write_logo(self, sink: str):
        """
        Writes the logo to the specified file.
        :param sink: Sink file path.
        :type sink: str
        :return: ...
        :rtype: ...
        """
        with open(sink, "w") as f:
            f.write(self.__logo)

    @staticmethod
    def trace(msg, *args, **kwargs):
        """
        Logs a trace message.

        :param msg: Message to log.
        :type msg: str
        :param args: ...
        :type args: ...
        :param kwargs: ...
        :type kwargs: ...
        :return: Logger object.
        :rtype: Logger
        """
        return logger.trace(msg, *args, **kwargs)

    @staticmethod
    def debug(msg, *args, **kwargs):
        """
        Logs a debug message.

        :param msg: Message to log.
        :type msg: str
        :param args: ...
        :type args: ...
        :param kwargs: ...
        :type kwargs: ...
        :return: Logger object.
        :rtype: Logger
        """
        return logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        """
        Logs an info message.

        :param msg: Message to log.
        :type msg: str
        :param args: ...
        :type args: ...
        :param kwargs: ...
        :type kwargs: ...
        :return: Logger object.
        :rtype: Logger
        """
        return logger.info(msg, *args, **kwargs)

    @staticmethod
    def success(msg, *args, **kwargs):
        """
        Logs a success message.

        :param msg: Message to log.
        :type msg: str
        :param args: ...
        :type args: ...
        :param kwargs: ...
        :type kwargs: ...
        :return: Logger object.
        :rtype: Logger
        """
        return logger.success(msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        """
        Logs a warning message.

        :param msg: Message to log.
        :type msg: str
        :param args: ...
        :type args: ...
        :param kwargs: ...
        :type kwargs: ...
        :return: Logger object.
        :rtype: Logger
        """
        return logger.warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        """
        Logs an error message.

        :param msg: Message to log.
        :type msg: str
        :param args: ...
        :type args: ...
        :param kwargs: ...
        :type kwargs: ...
        :return: Logger object.
        :rtype: Logger
        """
        return logger.error(msg, *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        """
        Logs a critical message.

        :param msg: Message to log.
        :type msg: str
        :param args: ...
        :type args: ...
        :param kwargs: ...
        :type kwargs: ...
        :return: Logger object.
        :rtype: Logger
        """
        return logger.critical(msg, *args, **kwargs)

    @staticmethod
    def exception(msg, *args, **kwargs):
        """
        Logs an exception.

        :param msg: Message to log.
        :type msg: str
        :param args: ...
        :type args: ...
        :param kwargs: ...
        :type kwargs: ...
        :return: Logger object.
        :rtype: Logger
        """
        return logger.exception(msg, *args, **kwargs)


journal: Journal = Journal(debug=True, serialize=True)
