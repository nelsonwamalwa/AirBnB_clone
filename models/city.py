#!/usr/bin/python3
""" Module: City
    
    Description: Defines the 'City()' as a sub_class of the BaseModel
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    Class: City class that holds the name and state id of the city 
    
    Attributes:
        name: string
        state_id: string
    """
    name = ""
    state_id = ""