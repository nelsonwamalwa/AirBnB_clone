#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User

AllObjects = storage.all()
print("-- Reloaded objects --")
for ObjectId in AllObjects.keys():
    obj = AllObjects[ObjectId]
    print(obj)

print("-- Create a new User --")
MyUser = User()
MyUser.first_name = "Betty"
MyUser.last_name = "Bar"
MyUser.email = "airbnb@mail.com"
MyUser.password = "root"
MyUser.save()
print(MyUser)

print("-- Create a new User 2 --")
MyUser2 = User()
MyUser2.first_name = "John"
MyUser2.email = "airbnb2@mail.com"
MyUser2.password = "root"
MyUser2.save()
print(MyUser2)
