from dinjectorr import inject, Injector


class A:
    def get_hello(self):
        return "Hello from A"


class B:
    @inject
    def __init__(self, a: A):
        self._a = a

    def get_hello(self):
        return self._a.get_hello()


class Client:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def get_api_key(self):
        return self._api_key


class CustomClient(Client):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def test_1():
    b = B()

    assert b.get_hello() == "Hello from A"


def test_2():
    Injector.register(Client, api_key="some_api_key")
    client = Injector.get_instance(Client)

    api_key = client.get_api_key()

    assert api_key == "some_api_key"


def test_3():
    Injector.register(CustomClient, api_key="some_api_key")
    custom_client = CustomClient()

    api_key = custom_client.get_api_key()

    assert api_key == "some_api_key"


def test_4():
    Injector.register(CustomClient, api_key="some_api_key")
    custom_client = CustomClient(api_key="another_api_key")

    api_key = custom_client.get_api_key()

    assert api_key == "another_api_key"
