from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.services.post_service import PostService, LikeService

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostRead)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = await PostService.create_post(
        db, current_user.id, data.content
    )
    return {
        **post.__dict__,
        "likes_count": 0,
    }


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: str,
    db: AsyncSession = Depends(get_db),
):
    post = await PostService.get_post(db, post_id)
    return {
        **post.__dict__,
        "likes_count": len(post.likes),
    }


@router.get("/", response_model=list[PostRead])
async def list_posts(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, le=100),
    offset: int = 0,
):
    rows = await PostService.list_posts(db, limit, offset)

    return [
        {
            **post.__dict__,
            "likes_count": likes_count,
        }
        for post, likes_count in rows
    ]


@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: str,
    data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = await PostService.get_post(db, post_id)

    updated = await PostService.update_post(
        db, post, data.content, current_user.id
    )

    return {
        **updated.__dict__,
        "likes_count": len(updated.likes),
    }

@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = await PostService.get_post(db, post_id)
    await PostService.delete_post(db, post, current_user.id)


@router.post("/{post_id}/like", status_code=204)
async def like_post(
    post_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await LikeService.like_post(db, current_user.id, post_id)


@router.delete("/{post_id}/like", status_code=204)
async def unlike_post(
    post_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await LikeService.unlike_post(db, current_user.id, post_id)


