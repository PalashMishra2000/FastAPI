from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, util
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#request comes in with a get method url : "/"




while True:    
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'Gungun29', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connection failed")
        print("Error: ", error)
        time.sleep(2)



my_posts = [{"title": "this is title 1", "content": "this is content1", "id": 1}, {"title":"favourite foods", "content":"I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"]== id:
            return p
    
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        
@app.include_router(post.router)
    
@app.get("/")
def root():
    return {"message": "Welcome world!!!!"}

#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
    #posts = db.query(models.Post).all()
    #print(posts)
    #return {"data": posts}


