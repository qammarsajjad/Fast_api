from pydantic import BaseModel
from typing import List, Union




class Blog(BaseModel):

    hotel_name:str

    address:str
    multi_type_hotel:str
    star_rating:Union[int, float, str]
    currency : str
    property_description:str
    property_highlights:Union[int, float, str]

class ShowBlog(BaseModel):
    hotel_name: str
    address:str
    class Config:
       orm_mode = True

class Contact(BaseModel):
    owner_nmb : int
    manger_nmb: int
    front_office_nmbr :int


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str

    class Config:
       orm_mode = True

  