from typing import Final
from logFormat import LogFormat
from logLevel import LogLevel
from providers import *

class Logger:

    # Static methods
    logLevels: Final[LogLevel] = LogLevel
    logFormats: Final[LogFormat] = LogFormat

    # The highest loglevel to output
    __highestLogLevel: LogLevel

    # The selected log provider
    __logProvider: Provider

    def __init__(self, logFormat: LogFormat):

        if logFormat == LogFormat.JSON:
            self.__logProvider = JsonProvider()
        elif logFormat == LogFormat.PLAIN_TEXT:
            self.__logProvider = PlainTextProvider()

    # Log method passing info to selected log provider
    def __log(self, level: LogLevel, message: str):
        # Do nothing if the current log level is larger than the highest loglevel
        if level > self.__highestLogLevel:
            return

        self.__logProvider.writeLog(level, message)


    # Helper methods for easy logging
    def fatal(self, message: str):
        self.__log(LogLevel.FATAL, message)

    def error(self, message: str):
        self.__log(LogLevel.ERROR, message)

    def warning(self, message: str):
        self.__log(LogLevel.WARNING, message)

    def info(self, message: str):
        self.__log(LogLevel.INFO, message)

    def debug(self, message: str):
        self.__log(LogLevel.DEBUG, message)
