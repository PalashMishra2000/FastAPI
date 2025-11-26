from fastapi import FastAPI
from fastapi.params import Body
from . import models
from .database import engine
from .routers import post, user, auth, vote

from app.config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#request comes in with a get method url : "/"
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome world!!!!"}

#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
    #posts = db.query(models.Post).all()
    #print(posts)
    #return {"data": posts}


