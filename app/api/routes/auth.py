from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.services.user_service import UserService
from app.core.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await UserService.create_user(
        db, user.email, user.username, user.password
    )
    token = create_access_token({"sub": new_user.id})
    return {"access_token": token}



@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
    ):
    user = await UserService.authenticate(
        db,
        email=form_data.username,
        password=form_data.password
    )

    token = create_access_token({"sub": str(user.id)})
    print(token)
    return {"access_token": token}
