from fastapi import FastAPI,Depends,status,Response,HTTPException,Body
from . import schemas,models
from .schemas import Contact
from .database import engine,SessionLocal
from sqlalchemy.orm import Session





app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():

    db = SessionLocal()
    try:
        yield db

    finally:

        db.close()


 

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db :Session =Depends(get_db)):
    new_blog = models.Blog(hotel_name=request.hotel_name,address=request.address,multi_type_hotel=request.multi_type_hotel,
    star_rating=request.star_rating,currency=request.currency,property_description=request.property_description,property_highlights=request.property_highlights 
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.post('/contact', status_code=status.HTTP_201_CREATED)
def create_contact(request:schemas.Contact,db :Session =Depends(get_db)):
    new_contact= models.Contact(owner_nmb=request.owner_nmb, manger_nmb=request.manger_nmb,front_office_nmbr=request.front_office_nmbr)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id,db :Session =Depends(get_db)):
        blog = db.query(models.Blog).filter(models.Blog.id == id)

        if not blog.first():

           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Blog wit this id {id} is not available')


        blog.delete(synchronize_session=False)
        db.commit()
        return 'Done'

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db :Session =Depends(get_db)):
     blog = db.query(models.Blog).filter(models.Blog.id == id)

     if not blog.first():
          
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Blog wit this id {id} is not available')
     
     blog.update(request.dict())

     db.commit()
     return f'Sucessfuly Updated!!!'
           

@app.get('/blog')
def all(db :Session =Depends(get_db)):

    blogs = db.query(models.Blog).all()

    return blogs

@app.get('/contact')
def all(db :Session =Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts


@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id, response:Response ,db :Session =Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} is not available")

    return blog
