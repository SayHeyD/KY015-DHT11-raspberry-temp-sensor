from logProvider import LogProviderMeta
from ..logLevel import LogLevel

class JsonProvider(LogProviderMeta):
    def writeLog(self, level: LogLevel, message):
        pass