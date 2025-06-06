from logProvider import LogProviderMeta
from ..logLevel import LogLevel

class PlainTextProvider(LogProviderMeta):
    def writeLog(self, level: LogLevel, message):
        pass