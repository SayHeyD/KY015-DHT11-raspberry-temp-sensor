# Parent class for LogProviders, used kinda like an interface
class LogProviderMeta(type):
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'writeLog') and
                callable(subclass.writeLog))