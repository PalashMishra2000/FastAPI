from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts ORDER BY id ASC""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all() 
    
    return posts 

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_users)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    
    return new_post
#title: str content: str

#@router.get("/posts/latest")
#def get_latest_posts():
#    post = my_posts[len(my_posts)-1]
#    return post

@router.get("/{id}", response_model=schemas.Post)
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
    return post
    
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}", response_model=schemas.Post)
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
    
    return post_query.first()
