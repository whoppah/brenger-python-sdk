from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, field_validator


class Contact(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str


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


class ItemSet(BaseModel):
    title: str
    items: List[Item]
    description: Optional[str] = None
    client_reference: Optional[str] = None


class ShipmentCreateRequest(BaseModel):
    item_sets: List[ItemSet]
    pickup: PickupDeliveryInfo
    delivery: PickupDeliveryInfo
    shipping_date: str

    @field_validator("shipping_date", mode="before")
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
