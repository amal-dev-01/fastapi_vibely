from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.profile import (
    ProfileCreate,
    ProfileRead,
    ProfileUpdate,
)
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileRead)
async def create_my_profile(
    data: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await ProfileService.create_profile(
        db,
        user_id=current_user.id,
        bio=data.bio,
        avatar_url=data.avatar_url,
    )


@router.get("/me", response_model=ProfileRead)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await ProfileService.get_by_user_id(db, current_user.id)


@router.put("/me", response_model=ProfileRead)
async def update_my_profile(
    data: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    profile = await ProfileService.get_by_user_id(db, current_user.id)

    return await ProfileService.update_profile(
        db,
        profile,
        bio=data.bio,
        avatar_url=data.avatar_url,
    )


@router.delete("/me", status_code=204)
async def delete_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    profile = await ProfileService.get_by_user_id(db, current_user.id)
    await ProfileService.delete_profile(db, profile)
