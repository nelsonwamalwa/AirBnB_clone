#!/usr/bin/python3
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

m_model = BaseModel()
m_model.name = "My First Model"
m_model.my_number = 89
print(m_model)
m_model.save()
print(m_model)
model_json = m_model.to_dict()
print(model_json)
print("JSON of m_model:")
for key in model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(model_json[key]), model_json[key]))
