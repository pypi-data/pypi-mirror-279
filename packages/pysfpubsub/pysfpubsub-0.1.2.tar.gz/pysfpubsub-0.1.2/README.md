# pysfpubsub

Python gRPC client for the Salesforce Pub/Sub API.

https://developer.salesforce.com/docs/platform/pub-sub-api/overview

### Installation

```
pip install pysfpubsub
```

### Usage

```
from datetime import datetime
from pysfpubsub import Client

def process_event(event, client):
    """
    This is a callback that gets passed to the `Client.subscribe()` method.
    When no events are received within a certain time period, the API's subscribe
    method sends keepalive messages and the latest replay ID through this callback.
    """
    if event.events:
        print("Number of events received in FetchResponse: ", len(event.events))
        # If all requested events are delivered, release the semaphore
        # so that a new FetchRequest gets sent by `Client.fetch_req_stream()`.
        if event.pending_num_requested == 0:
            client.release_subscription_semaphore()

        for evt in event.events:
            # Get the event payload and schema, then decode the payload
            payload_bytes = evt.event.payload
            json_schema = client.get_schema_json(evt.event.schema_id)
            decoded_event = client.decode(json_schema, payload_bytes)
            print(decoded_event)
    else:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] The subscription is active.")

config = {
    "url": "https://login.salesforce.com",
    "username": "myusername",
    "password": "mypassword",
    "grpc_host": "api.pubsub.salesforce.com",
    "grpc_port": 7443,
    "api_version": "57.0"
}
sfdc_handler = Client(**config)
sfdc_handler.auth()
sfdc_handler.subscribe("/events/Example_Event__c", "LATEST", "", 1, process_event)
```