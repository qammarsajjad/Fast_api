from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schemas,models
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
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

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

@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
def show(id, response:Response ,db :Session =Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} is not available")

    return blog
