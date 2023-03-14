from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/blog')
def index(limit=10,published: bool=False,sort:Optional[str] =None):
    if published:

        return {'data':f'{limit} Published Blogs From DB'}
    else:
         return {'data':f'{limit} Blogs From DB'}


@app.get('/blog/unpublished-blog')
def unpublished():
    return{'data':'blog is unpublished'}

@app.get('/blog/{id}/')
def about(id: int):
    return {'data':id}


@app.get('/blog/{id}/comments')
def comments(id: int,limit=10):
    return {'comments':limit}

class Blog(BaseModel):
    title:str
    body:str
    published : Optional[bool]

@app.post('/blogs/')
def create_blog(request: Blog):

    return {'data':f'Blog is created title as_ {request.title}'}

