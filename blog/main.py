from fastapi import FastAPI,Depends,status,Response,HTTPException,Body
from . import schemas,models
from .schemas import Contact
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext





app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():

    db = SessionLocal()
    try:
        yield db

    finally:

        db.close()


 

@app.post('/blog', status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request:schemas.Blog,db :Session =Depends(get_db)):
    new_blog = models.Blog(hotel_name=request.hotel_name,address=request.address,multi_type_hotel=request.multi_type_hotel,
    star_rating=request.star_rating,currency=request.currency,property_description=request.property_description,property_highlights=request.property_highlights 
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.post('/contact', status_code=status.HTTP_201_CREATED,tags=['contacts'])
def create_contact(request:schemas.Contact,db :Session =Depends(get_db)):
    new_contact= models.Contact(owner_nmb=request.owner_nmb, manger_nmb=request.manger_nmb,front_office_nmbr=request.front_office_nmbr)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def delete(id,db :Session =Depends(get_db)):
        blog = db.query(models.Blog).filter(models.Blog.id == id)

        if not blog.first():

           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Blog wit this id {id} is not available')


        blog.delete(synchronize_session=False)
        db.commit()
        return 'Done'

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id,request:schemas.Blog,db :Session =Depends(get_db)):
     blog = db.query(models.Blog).filter(models.Blog.id == id)

     if not blog.first():
          
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Blog wit this id {id} is not available')
     
     blog.update(request.dict())

     db.commit()
     return f'Sucessfuly Updated!!!'
           

@app.get('/blog',response_model=List[schemas.ShowBlog],tags=['blogs'])
def all(db :Session =Depends(get_db)):

    blogs = db.query(models.Blog).all()

    return blogs

@app.get('/contact',tags=['contacts'])
def all(db :Session =Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts


@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog,tags=['blogs'])
def show(id, response:Response ,db :Session =Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} is not available")

    return blog


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user/',response_model=schemas.ShowUser,tags=['users'])
def create_user(request: schemas.User,db :Session =Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User( name=request.name, email=request.email, password= hashedPassword )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}',response_model=schemas.ShowUser,tags=['users'])
def get_user(id:int,db :Session =Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The User wit id  {id} is not available")
    
    return user