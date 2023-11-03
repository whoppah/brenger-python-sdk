# Brenger API Client

This Python package provides an interface to interact with the Brenger API, facilitating shipment operations like creating and retrieving shipments. It includes Pydantic models for data validation, a client for API communication, custom exceptions for error handling, and model validations.

## Requirements

- Requests library
- Pydantic library

## Installation
`$ poetry add brenger-python-sdk` 

## Structure
The package consists of the following components:

**BrengerAPIClient**: A client class to send HTTP requests to the Brenger API.

**Models**: Pydantic classes used for request validation and response parsing.

**Exceptions**: Custom exception classes for handling API errors.

**Logging**: Pre-configured logging for monitoring the API interactions.

## Usage

**Setting Up the Client**

To use the `BrengerAPIClient`, instantiate it with your API key and namespace:

```python
from brenger.client import BrengerAPIClient

client = BrengerAPIClient(api_key='your_api_key', namespace='your_namespace')
# according to docs unless specified namespace is 'v1' so we are using 'v1'
```

**Creating a Shipment**

Create a shipment by constructing a ShipmentCreateRequest object and passing it to the create_shipment method:

```python
from brenger.models import ShipmentCreateRequest, PickupDeliveryInfo, ItemSet

shipment_data = ShipmentCreateRequest(
    item_sets=[...],  # List of ItemSet instances
    pickup=PickupDeliveryInfo(...),  # Pickup details
    delivery=PickupDeliveryInfo(...),  # Delivery details
    shipping_date='YYYY-MM-DD'  # Shipping date as a string, or date object. We will convert it to 'YYYY-MM-DD' format
)

shipment_response = client.create_shipment(shipment_data)
```
**Retrieving a Shipment**

Retrieve details of a specific shipment by its ID:

```python
shipment_id = 'some_shipment_id'
shipment_details = client.get_shipment(shipment_id)
```

**Handling Exceptions**

Handle potential exceptions using the custom exception classes:

```python
from brenger.exceptions import APIClientError, APIServerError

try:
    shipment_response = client.create_shipment(shipment_data)
except APIClientError as e:
    print(f'Client error occurred: {e}')
except APIServerError as e:
    print(f'Server error occurred: {e}')
```

**Models**

Refer to the models defined in `brenger.models` for constructing request payloads and understanding response data.

**Testing**

Ensure to write tests for your implementation, validating the behavior of the client under various scenarios.
Current tests and `dummy data` can be found under tests/ folder. 