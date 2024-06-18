# dinjectorr
A simple dependency injector for Python.

## Installation
```bash
pip install dinjectorr
```

## Usage
Example 1:
```python
from dinjectorr import inject

class A:
    def print_hello(self):
        print("Hello from A")

class B:
    @inject
    def __init__(self, a: A):
        self._a = a

    def print_hello(self):
        self._a.print_hello()

b = B()
b.print_hello()
# Output:
# Hello from A
```
Example 2:
```python
from dinjectorr import Injector

class Client:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def print_api_key(self):
        print(self._api_key)

Injector.register(Client, api_key="some_api_key")
client = Injector.get_instance(Client)
client.print_api_key()
# Output:
# some_api_key
```
Example 3:
```python
from dinjectorr import inject, Injector

class Client:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def print_api_key(self):
        print(self._api_key)

class CustomClient(Client):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

Injector.register(CustomClient, api_key="some_api_key")
custom_client = CustomClient()
custom_client.print_api_key()
# Output:
# some_api_key
```
Example 4:
```python
from dinjectorr import inject, Injector

class Client:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def print_api_key(self):
        print(self._api_key)

class CustomClient(Client):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

Injector.register(CustomClient, api_key="some_api_key")
custom_client = CustomClient(api_key="another_api_key")
custom_client.print_api_key()
# Output:
# another_api_key
```
