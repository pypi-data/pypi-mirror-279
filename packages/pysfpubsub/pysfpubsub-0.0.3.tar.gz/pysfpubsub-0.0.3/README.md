# pysfpubsub
Python gRPC client for the Salesforce Pub/Sub API.

https://developer.salesforce.com/docs/platform/pub-sub-api/overview

### Environment Variables

The following environment variables are required:

```
grpc_host="api.pubsub.salesforce.com"
grpc_port=7443
topic="/event/Your_Event__e"
password='yourpassword'
user="your@domain.com"
url="https://login.salesforce.com"
api_version="57.0"
```

### Example implementation

```
import libs.pubsub_api_pb2 as pb2
import logging
from datetime import datetime
from libs.pubsub import PubSub
from models.settings import Settings


def process_event(event: pb2.FetchResponse, pubsub: PubSub) -> None:
    """
    This is a callback that gets passed to the `PubSub.subscribe()` method.
    When no events are received within a certain time period, the API's subscribe
    method sends keepalive messages and the latest replay ID through this callback.
    """
    if event.events:
        print("Number of events received in FetchResponse: ", len(event.events))
        # If all requested events are delivered, release the semaphore
        # so that a new FetchRequest gets sent by `PubSub.fetch_req_stream()`.
        if event.pending_num_requested == 0:
            pubsub.release_subscription_semaphore()

        for evt in event.events:
            # Get the event payload and schema, then decode the payload
            payload_bytes = evt.event.payload
            json_schema = pubsub.get_schema_json(evt.event.schema_id)
            decoded_event = pubsub.decode(json_schema, payload_bytes)
            logging.info(f"Received Event: \n{decoded_event}")
    else:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] The subscription is active.")

def run(settings: Settings) -> None:
    sfdc_handler = PubSub(settings)
    sfdc_handler.auth()
    sfdc_handler.subscribe(settings.TOPIC, "LATEST", "", 1, process_event)


if __name__ == "__main__":
    settings = Settings()
    logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
    logging.debug(settings)
    run(settings)
```