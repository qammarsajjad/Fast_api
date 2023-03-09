from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data':{'name':'Qammar Sajjad'}}

@app.get('/about')
def about():
    return {'data':{'About Page'}}
