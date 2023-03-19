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
    class Config:
       orm_mode = True

class Contact(BaseModel):
    owner_nmb : int
    manger_nmb: int
    front_office_nmbr :int

