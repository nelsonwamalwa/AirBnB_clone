#!/usr/bin/python3
from models.base_model import BaseModel

MyModel = BaseModel()
MyModel.name = "My_First_Model"
MyModel.my_number = 89
print(MyModel.id)
print(MyModel)
print(type(MyModel.created_at))
print("--")
JsonModel = MyModel.to_dict()
print(JsonModel)
print("JSON of MyModel:")
for key in JsonModel.keys():
    print("\t{}: ({}) - {}".format(key, type(JsonModel[key]), JsonModel[key]))

print("--")
NewModel = BaseModel(**JsonModel)
print(NewModel.id)
print(NewModel)
print(type(NewModel.created_at))

print("--")
print(MyModel is NewModel)
