from operator import ge
from .. import models, schemas, utils, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = ""):
    # curr.execute("SELECT * FROM posts")
    # posts = curr.fetchall()
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return(results)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #              (post.title, post.content, post.published))
    # new_post = curr.fetchone()
    # # have to commit the data
    # conn.commit()
    print(current_user.id)
    print(current_user.email)
    # the ** post.dict gets us all the info in the right format to pass to model
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # pushing post to the db
    db.add(new_post)
    db.commit()
    # returning in orm (retreieve the post)
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
# we automatically get the id and can pass to function
# adding : int will add validation so they cannot pass junk
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # id_post = curr.fetchone()
    # use .filter to get specific post if we know there is only one use .first
    id_post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if id_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
    # deleted_post = curr.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')

    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    # cannot pass .first to deleted post before if have to keep it a query
    # to be able to call .delete
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
# use schema again so front end cannot send whatever
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #              (post.title, post.content, post.published, str(id)))
    # updated_post = curr.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()
