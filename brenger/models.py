from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator, validator


def strip_whitespace(cls, value: Any):
    """
    Brenger API is failing if strings are ends with emtpy space lol.

    Strip whitespace from string fields.
    """
    if isinstance(value, str):
        return value.rstrip()
    return value


class Contact(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str

    _strip_whitespace = field_validator(
        "first_name", "last_name", "email", "phone", mode="before"
    )(strip_whitespace)

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def check_name_length(cls, value: str) -> str:
        """
        Brenger API has validation for first name and last name to be min 3 characters.

        Validation makes sure that if the length of the name is less than 3, it is padded with dots.
        """
        if len(value) < 3:
            value += "." * (4 - len(value))
        return value


class Address(BaseModel):
    type: str
    line1: str
    line2: Optional[str] = None
    postal_code: str
    locality: str
    administrative_area: str
    country_code: str
    lat: Optional[float] = None
    lng: Optional[float] = None

    _strip_whitespace = field_validator(
        "line1", "line2", "postal_code", "locality", mode="before"
    )(strip_whitespace)


class Details(BaseModel):
    situation: str
    floor_level: int
    elevator: bool
    extra_carrying_help: Optional[bool] = False
    instructions: Optional[str] = None


class PickupDeliveryInfo(BaseModel):
    contact: Contact
    address: Address
    details: Details


class Item(BaseModel):
    title: str
    length: int
    height: int
    width: int
    count: int
    weight: Optional[int] = None
    _strip_whitespace = field_validator("title", mode="before")(strip_whitespace)


class ItemSet(BaseModel):
    title: str
    items: List[Item]
    description: Optional[str] = None
    client_reference: Optional[str] = None

    _strip_whitespace = field_validator("title", "description", mode="before")(
        strip_whitespace
    )


class ShipmentCreateRequest(BaseModel):
    item_sets: List[ItemSet]
    pickup: PickupDeliveryInfo
    delivery: PickupDeliveryInfo
    shipping_date: str

    @validator("shipping_date", pre=True)
    def validate_shipping_date(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        elif isinstance(value, str):
            try:
                parsed_date = date.fromisoformat(value)
                return parsed_date.isoformat()
            except ValueError:
                raise ValueError(
                    f"shipping_date must be a valid 'YYYY-MM-DD' formatted string, received {value}"
                )
        else:
            raise TypeError(
                "shipping_date must be a date object or a 'YYYY-MM-DD' formatted string"
            )


class TimeWindow(BaseModel):
    start: str
    end: str
    timezone: str


class Price(BaseModel):
    excl_vat: int
    incl_vat: int
    vat: int
    currency: str


class ShippingLabel(BaseModel):
    pdf: str


class ShipmentResponse(BaseModel):
    id: str
    pickup_time_window: Optional[TimeWindow]
    delivery_time_window: Optional[TimeWindow]
    price: Optional[Price]
    shipped_by: Optional[Dict]
    shipping_date: str
    shipping_label: Optional[ShippingLabel]
    state: str
    tracking_id: str
    tracking_url: str
    tracking_urls: Dict[str, str]

    class Config:
        extra = "ignore"


# ============================================================================
# V2 API Models
# ============================================================================


class V2Address(BaseModel):
    country: str
    administrative_area: Optional[str] = None
    locality: str
    postal_code: str
    line1: str
    line2: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

    _strip_whitespace = field_validator(
        "line1", "line2", "postal_code", "locality", mode="before"
    )(strip_whitespace)


class V2Stop(BaseModel):
    email: str
    phone_number: Optional[str] = None
    instructions: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    preferred_locale: Optional[str] = None
    address: V2Address

    _strip_whitespace = field_validator(
        "email", "first_name", "last_name", "company_name", mode="before"
    )(strip_whitespace)


class V2Item(BaseModel):
    title: str
    category: str = "other"
    images: Optional[List[str]] = None
    width: int
    height: int
    length: int
    count: int

    _strip_whitespace = field_validator("title", "category", mode="before")(
        strip_whitespace
    )


class V2Amount(BaseModel):
    currency: str
    value: str


class V2Price(BaseModel):
    vat: V2Amount
    incl_vat: V2Amount
    excl_vat: V2Amount


class V2Feasible(BaseModel):
    value: bool
    reasons: List[str]


class V2QuoteRequest(BaseModel):
    pickup: Dict
    delivery: Dict
    external_reference: Optional[str] = None
    items: List[V2Item]


class V2QuoteResponse(BaseModel):
    price: V2Price
    feasible: V2Feasible
    pickup: Dict
    delivery: Dict
    external_reference: Optional[str] = None
    items: List[V2Item]

    class Config:
        extra = "ignore"


class V2ShipmentCreateRequest(BaseModel):
    pickup: V2Stop
    delivery: V2Stop
    external_reference: str
    external_listing_url: Optional[str] = None
    external_private_url: Optional[str] = None
    items: List[V2Item]
    price: Optional[V2Price] = None


class V2ShipmentCreateResponse(BaseModel):
    shipment_id: str
    pickup: V2Stop
    delivery: V2Stop
    pickup_url: str
    delivery_url: str
    shipment_url: str
    external_reference: str
    external_listing_url: Optional[str] = None
    external_private_url: Optional[str] = None
    items: List[V2Item]
    price: V2Price

    class Config:
        extra = "ignore"


class V2Event(BaseModel):
    id: str
    timestamp: str
    status: str


class V2StatusResponse(BaseModel):
    shipment_id: str
    external_reference: str
    status: str
    events: List[V2Event]

    class Config:
        extra = "ignore"


class V2RefundResponse(BaseModel):
    refund_id: str
    amount: V2Price
    code: str

    class Config:
        extra = "ignore"


class V2WebhookPayload(BaseModel):
    event_id: str
    shipment_id: str
    external_reference: str
    timestamp: str
    status: str
