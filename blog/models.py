from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String




class Blog(Base):
    __tablename__='blogs'
    id = Column(Integer,primary_key=True,index=True)
    hotel_name = Column(String)
    address= Column(String)
    multi_type_hotel =Column(String)
    star_rating=int
    currency = Column(String)
    property_description=Column(String)
    property_highlights= int


class Contact(Base):
    __tablename__='contacts'
    id = Column(Integer,primary_key=True,index=True)
    owner_nmb = int
    manger_nmb= int
    front_office_nmbr = int

class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String,unique=True,index=True)
    password = Column(String)
    










