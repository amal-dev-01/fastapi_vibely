from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.user import User
from app.core.security import hash_password, verify_password
from datetime import datetime

class UserService:

    @staticmethod
    async def create_user(db: AsyncSession, email: str, username: str, password: str):
        result = await db.execute(select(User).where(User.email == email))
        if result.scalar():
            raise HTTPException(status_code=400, detail="Email already registered")
        now = datetime.now()
        user = User(
            email=email,
            username=username,
            password_hash=hash_password(password),
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user
