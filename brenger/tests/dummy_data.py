from datetime import date

from brenger.models import (
    Address,
    Contact,
    Details,
    Item,
    ItemSet,
    PickupDeliveryInfo,
    Price,
    ShipmentCreateRequest,
    ShipmentResponse,
    ShippingLabel,
    TimeWindow,
)

pickup_contact = Contact(
    first_name="John", last_name="Doe", email="johndoe@example.com", phone="0612345678"
)

delivery_contact = Contact(
    first_name="Jane  ",
    last_name="Smith  ",
    email="janesmith@example.com",
    phone="0698765432",
)

pickup_address = Address(
    type="depot",
    line1="123 Pickup Street   ",
    line2=None,
    postal_code="1001",
    locality="Pickup City",
    administrative_area="Pickup Area",
    country_code="NL",
    lat=52.3676,
    lng=4.9041,
)

delivery_address = Address(
    type="customer",
    line1="456 Delivery Avenue",
    line2="Apt 789",
    postal_code="2002",
    locality="Delivery City",
    administrative_area="Delivery Area",
    country_code="NL",
    lat=52.3676,
    lng=4.9041,
)


pickup_details = Details(
    situation="store",
    floor_level=0,
    elevator=False,
    extra_carrying_help=False,
    instructions="Handle with care.",
)

delivery_details = Details(
    situation="home",
    floor_level=1,
    elevator=True,
    extra_carrying_help=False,
    instructions="Ring the doorbell twice.",
)


pickup_info = PickupDeliveryInfo(
    contact=pickup_contact, address=pickup_address, details=pickup_details
)

delivery_info = PickupDeliveryInfo(
    contact=delivery_contact, address=delivery_address, details=delivery_details
)

item = Item(title="Office Chair", length=120, height=65, width=60, count=1, weight=15)

item_set = ItemSet(
    title="Office Furniture",
    items=[item],
    description="A set of office furniture items",
    client_reference="REF123456",
)

shipment_create_request = ShipmentCreateRequest(
    item_sets=[item_set],
    pickup=pickup_info,
    delivery=delivery_info,
    shipping_date=str(date.today()),
)

shipment_response = ShipmentResponse(
    id="d25d7a1b-0a6f-43c5-8a44-15b88ca535a8",
    pickup_time_window=TimeWindow(
        start="08:00:00", end="18:00:00", timezone="Europe/Amsterdam"
    ),
    delivery_time_window=TimeWindow(
        start="09:00:00", end="18:00:00", timezone="Europe/Amsterdam"
    ),
    price=Price(excl_vat=1827, incl_vat=2210, vat=383, currency="EUR"),
    shipped_by=None,
    shipping_date="2023-11-06",
    shipping_label=ShippingLabel(
        pdf="/v1/shipments/d25d7a1b-0a6f-43c5-8a44-15b88ca535a8/shipping_label.pdf"
    ),
    state="ready_for_pickup",
    tracking_id="a535a8",
    tracking_url="https://live.brenger.nl/sandbox/d25d7a1b-0a6f-43c5-8a44-15b88ca535a8",
    tracking_urls={
        "delivery": "https://live.brenger.nl/sandbox/66267190-d170-4723-bcfc-f9ee663a5798",
        "full": "https://live.brenger.nl/sandbox/d25d7a1b-0a6f-43c5-8a44-15b88ca535a8",
        "pickup": "https://live.brenger.nl/sandbox/b78b4b46-3b62-4619-8851-27eed2e7a669",
    },
)

shipment_response_json = {
    "delivery": {
        "address": {
            "administrative_area": "Delivery Area",
            "country_code": "NL",
            "lat": 52.3676,
            "line1": "456 Delivery Avenue",
            "line2": "Apt 789",
            "lng": 4.9041,
            "locality": "Delivery City",
            "postal_code": "2002",
        },
        "contact": {
            "email": "janesmith@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "0698765432",
        },
        "details": {
            "elevator": True,
            "extra_carrying_help": False,
            "floor_level": 1,
            "instructions": "Ring the doorbell twice.",
            "situation": "home",
        },
    },
    "delivery_time_window": {
        "end": "18:00:00",
        "start": "09:00:00",
        "timezone": "Europe/Amsterdam",
    },
    "id": "d25d7a1b-0a6f-43c5-8a44-15b88ca535a8",
    "item_sets": [
        {
            "client_reference": "REF123456",
            "description": "A set of office furniture items",
            "extra_services": [],
            "items": [
                {
                    "count": 1,
                    "height": 65,
                    "length": 120,
                    "title": "Office Chair",
                    "weight": 15,
                    "width": 60,
                }
            ],
            "title": "Office Furniture",
        }
    ],
    "pickup": {
        "address": {
            "administrative_area": "Pickup Area",
            "country_code": "NL",
            "lat": 52.3676,
            "line1": "123 Pickup Street",
            "line2": "",
            "lng": 4.9041,
            "locality": "Pickup City",
            "postal_code": "1001",
        },
        "contact": {
            "email": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "0612345678",
        },
        "details": {
            "elevator": False,
            "extra_carrying_help": False,
            "floor_level": 0,
            "instructions": "Handle with care.",
            "situation": "store",
        },
    },
    "pickup_time_window": {
        "end": "18:00:00",
        "start": "08:00:00",
        "timezone": "Europe/Amsterdam",
    },
    "price": {"currency": "EUR", "excl_vat": 1827, "incl_vat": 2210, "vat": 383},
    "shipped_by": None,
    "shipping_date": "2023-11-06",
    "shipping_label": {
        "pdf": "/v1/shipments/d25d7a1b-0a6f-43c5-8a44-15b88ca535a8/shipping_label.pdf"
    },
    "state": "ready_for_pickup",
    "tracking_id": "a535a8",
    "tracking_url": "https://live.brenger.nl/d25d7a1b-0a6f-43c5-8a44-15b88ca535a8",
    "tracking_urls": {
        "delivery": "https://live.brenger.nl/66267190-d170-4723-bcfc-f9ee663a5798",
        "full": "https://live.brenger.nl/d25d7a1b-0a6f-43c5-8a44-15b88ca535a8",
        "pickup": "https://live.brenger.nl/b78b4b46-3b62-4619-8851-27eed2e7a669",
    },
}
