from datetime import date
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, validator, field_validator


def strip_whitespace(cls, value: Any):
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
