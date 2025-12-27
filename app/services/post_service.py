from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.models.profile import Profile
from app.models.post import Post, Like
from sqlalchemy import func


class PostService:

    @staticmethod
    async def create_post(
        db: AsyncSession,
        user_id: str,
        content: str | None = None
    ):
        post = Post(
            user_id=user_id,
            content=content,
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def get_post(db: AsyncSession, post_id: str) -> Post:
        result = await db.execute(
            select(Post).where(Post.id == post_id)
        )
        post = result.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    

    @staticmethod
    async def list_posts(db: AsyncSession, limit: int = 20, offset: int = 0):
        result = await db.execute(
            select(
                Post,
                func.count(Like.id).label("likes_count")
            )
            .outerjoin(Like)
            .group_by(Post.id)
            .order_by(Post.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.all()


    @staticmethod
    async def update_post(
        db: AsyncSession,
        post: Post,
        content: str | None,
        current_user_id: str,

    ):
        if post.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )

        post.content = content
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def delete_post(db: AsyncSession, post: Post, current_user_id: str):
        if post.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )
        await db.delete(post)
        await db.commit()



class LikeService:

    @staticmethod
    async def like_post(
        db: AsyncSession,
        user_id: str,
        post_id: str

        ):
        print(user_id,post_id,'erjjergbeb')
        result = await db.execute(
            select(Like).where(
                Like.user_id == user_id,
                Like.post_id == post_id,
            )
        )
        if result.scalar():
            raise HTTPException(status_code=400, detail="Already liked")


        like = Like(user_id=user_id, post_id=post_id)
        db.add(like)
        await db.commit()


    @staticmethod
    async def unlike_post(
        db: AsyncSession,
        user_id: str, 
        post_id: str
        ):

        result = await db.execute(
            select(Like).where(
                Like.user_id == user_id,
                Like.post_id == post_id,
            )
        )

        like = result.scalar_one_or_none()
        if not like:
            raise HTTPException(status_code=404, detail="Like not found")

        await db.delete(like)
        await db.commit()
