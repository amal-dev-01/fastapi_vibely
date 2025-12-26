from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.models.profile import Profile


class ProfileService:

    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: str):
        result = await db.execute(
            select(Profile).where(Profile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    @staticmethod
    async def create_profile(
        db: AsyncSession,
        user_id: str,
        bio: str | None = None,
        avatar_url: str | None = None
    ):
        profile = Profile(
            user_id=user_id,
            bio=bio,
            avatar_url=avatar_url,
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile

    @staticmethod
    async def update_profile(
        db: AsyncSession,
        profile: Profile,
        bio: str | None,
        avatar_url: str | None
    ):
        if bio is not None:
            profile.bio = bio
        if avatar_url is not None:
            profile.avatar_url = avatar_url

        await db.commit()
        await db.refresh(profile)
        return profile

    @staticmethod
    async def delete_profile(db: AsyncSession, profile: Profile):
        await db.delete(profile)
        await db.commit()
