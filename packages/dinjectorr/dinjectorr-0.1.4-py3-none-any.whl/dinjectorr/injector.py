class Injector:
    type_kwargs = {}

    @staticmethod
    def register(type_, **kwargs):
        Injector.type_kwargs[type_.__name__] = kwargs

    @staticmethod
    def get_instance(type_):
        kwargs = Injector.type_kwargs.get(type_.__name__, {})
        return type_(**kwargs)
