from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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
    
@app.get("/")
def root():
    return {"message": "Welcome world!!!!"}

#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
    #posts = db.query(models.Post).all()
    #print(posts)
    #return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts ORDER BY id ASC""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all() 
    
    return {"data": posts} 

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    
    return {"data": new_post}
#title: str content: str

@app.get("/posts/latest")
def get_latest_posts():
    post = my_posts[len(my_posts)-1]
    return post

@app.get("/posts/{id}")
def get_post(id:int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    #test_post = cursor.fetchone()
    #print(test_post)
    #post = find_post(id)
    
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id: {id} was not found"}
    return {"post_detail": post}
    
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    #cursor.execute("""DELETE FROM posts WHERE ID = %s RETURNING *""", (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id==id)
    
    if post.first == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} was not found!")
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id : int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published,(str(id))))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} was not found!")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
    
    
         