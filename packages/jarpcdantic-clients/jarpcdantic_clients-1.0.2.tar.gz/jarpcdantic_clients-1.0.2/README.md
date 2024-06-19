# JARPCdantic clients

JARPCdantic client's factories with predefined transports for libraries: cabbagok, aiohttp, requests.


## Installation
```sh
# with cabbagok dependency
pip install jarpcdatic_clients[cabbagok]
# with aiohttp
pip install jarpcdatic_clients[aiohttp]
# with requests
pip install jarpcdatic_clients[requests]
# with all dependencies
pip install jarpcdatic_clients[all]
```

## Usage

1) Choose desired transport and install required packages (this library's installation doesn't include transport-dependent packages);
2) Use factory to create JARPCdantic client or use transport separately:

```python
from jarpcdantic_clients import create_cabbage_client

amqp_rpc = ...
client = create_cabbage_client(amqp_rpc=amqp_rpc, exchange='exchange_name', default_ttl=30.0)
result = client(method='method_name', params=dict(param1=1))
result = client.method_name(param1=1)
```

```python
from jarpc import JarpcClient
from jarpcdantic_clients import RequestsTransport

transport = RequestsTransport(url='http://example.com/jarpc')
client = JarpcClient(transport=transport)
result = client(method='method_name', params=dict(param1=1))
result = client.method_name(param1=1)
transport.close_session()
```
