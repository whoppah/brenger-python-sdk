import logging

import requests
from requests import Response

from .exceptions import APIClientError, APIServerError
from .models import ShipmentCreateRequest, ShipmentResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://external-api.brenger.nl/{namespace}"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


class BrengerAPIClient:
    def __init__(self, api_key: str, namespace: str) -> None:
        self.api_key = api_key
        self.namespace = namespace
        self.session = requests.Session()
        self.session.headers.update({"X-AUTH-TOKEN": self.api_key, **HEADERS})

    def create_shipment(self, shipment_data: ShipmentCreateRequest) -> ShipmentResponse:
        url = BASE_URL.format(namespace=self.namespace) + "/shipments"
        response = self.session.post(
            url, data=shipment_data.model_dump_json().encode("utf-8")
        )
        self._handle_response_errors(response)
        logger.info(
            "Shipment created successfully with ID: %s", response.json().get("id")
        )
        return ShipmentResponse(**response.json())

    def get_shipment(self, shipment_id: str) -> ShipmentResponse:
        url = BASE_URL.format(namespace=self.namespace) + f"/shipments/{shipment_id}"
        response = self.session.get(url)
        self._handle_response_errors(response)
        logger.info("Shipment details retrieved successfully for ID: %s", shipment_id)
        return ShipmentResponse(**response.json())

    def _handle_response_errors(self, response: Response) -> None:
        if response.status_code == 500:
            logger.error("Server Error")
            raise APIServerError("Internal Server Error")
        elif response.status_code >= 400:
            response_json = response.json()
            error_description = response_json.get("description", "An error occurred")
            error_hint = response_json.get("hint", "Hint not provided")
            error_validation = response_json.get(
                "validation_errors", "Validation not provided"
            )
            error_message = (
                f" Status code: {response.status_code} - "
                f"Error description: {error_description} -"
                f" Error hint: {error_hint} - "
                f" validation errors: {error_validation}"
            )
            logger.error(f"Client Error: {error_message}")
            raise APIClientError(f"Client Error: {error_message}")
        response.raise_for_status()
