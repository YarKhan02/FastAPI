from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session, aliased
from sqlalchemy import func

from typing import List, Optional

from .. import models, schemas, outh2
from ..database import get_db


router = APIRouter(prefix = '/posts', tags = ['Posts'])


@router.get('/', response_model = List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts
    

@router.get('/my', response_model = List[schemas.PostVote])
def get_my_posts(response: Response, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()

    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {current_user.id} not found')

    return posts


@router.get('/friends/{id}', response_model = List[schemas.PostVote])
def get_friends_posts(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.owner_id == id).all()

    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} not found')

    return posts


@router.get('/{id}', response_model = schemas.PostVote)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {current_user.id} not found')

    return post


@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict()) # **post.dict() unpack all fields
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post 


@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} does not exist')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perform requested action')

    query.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code = status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post_u = query.first()

    if post_u == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} does not exist')

    if post_u.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perform requested action')

    query.update(post.dict(), synchronize_session = False)
    db.commit()

    return query.first()