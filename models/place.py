#!/usr/bin/python3
"""The `place` module

It defines one class, `Place(),
which sub-classes the `BaseModel()` class.`
"""
from models.base_model import BaseModel


class Place(BaseModel):
    """A place/house in the application.

    It represents a place/house uploaded
    by the users of the application.

    Attributes:
        name
        user_id
        city_id
        description
        number_bathrooms
        price_by_night
        number_rooms
        longitude
        latitude
        max_guest
        amenity_ids
    """

    name: str
    user_id: str
    city_id: str
    description: str
    number_bathrooms: int
    price_by_night: int
    number_rooms: int
    longitude: float
    latitude: float
    max_guest: int
    amenity_ids: list