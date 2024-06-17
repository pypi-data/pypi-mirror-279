# Ambient Event Bus Client

## Typical usage example

```python
from ambient_event_bus_client import Client, ClientOptions

options = ClientOptions(
    event_api_url="http://localhost:8000",
    connection_service_url="http://localhost:8001",
    api_token = "my_token"
)
client = Client(options)
await client.init_client() # ensure you are in an async context

# add subscriptions
await client.add_subscription(topic="test")

# read messages from subscriptions
async for message in client.subscribe():
    print(message)

# publish a message
message = MessageCreate(topic="my_topic", message="my_message")
await client.publish(message)
```
