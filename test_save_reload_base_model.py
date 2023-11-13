#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel

AllObjects = storage.all()
print("-- Reloaded objects --")
for ObjectId in AllObjects.keys():
    obj = AllObjects[ObjectId]
    print(obj)

print("-- Create a new object --")
MyModel = BaseModel()
MyModel.name = "My_First_Model"
MyModel.my_number = 89
MyModel.save()
print(MyModel)
