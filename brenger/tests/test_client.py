import unittest
from unittest.mock import patch

from brenger.client import BrengerAPIClient
from brenger.exceptions import APIClientError
from brenger.tests import dummy_data


class TestBrengerAPIClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test-api-key"
        self.namespace = "test-namespace"
        self.client = BrengerAPIClient(api_key=self.api_key, namespace=self.namespace)
        self.test_shipment_data = dummy_data.shipment_create_request

    @patch("brenger.client.requests.Session.post")
    def test_create_shipment_success(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = dummy_data.shipment_response_json

        response = self.client.create_shipment(self.test_shipment_data)
        self.assertEqual(response.id, dummy_data.shipment_response.id)

    @patch("brenger.client.requests.Session.get")
    def test_get_shipment_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = dummy_data.shipment_response_json

        response = self.client.get_shipment(dummy_data.shipment_response.id)
        self.assertEqual(response.id, dummy_data.shipment_response.id)

    @patch("brenger.client.requests.Session.post")
    def test_api_error_handling(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 400
        mock_response.json.return_value = {"description": "Invalid request parameters"}

        with self.assertRaises(APIClientError) as context:
            self.client.create_shipment(self.test_shipment_data)

        self.assertIn("Client Error:  Status code: 400", str(context.exception))
