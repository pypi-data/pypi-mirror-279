# dinjector

A simple dependency injector for Python.

## Installation

You can install the package using pip:

```sh
pip install dinjector

Usage
Here's an example of how to use dinjector:

```python
from dinjector.injector import Injector, inject

class Service:
    def __init__(self, config):
        self.config = config

class Config:
    pass

Injector.register(Service, config=Config())

class Client:
    @inject
    def __init__(self, service: Service):
        self.service = service

client = Client()
print(client.service)  # Instance of Service with injected Config
```
