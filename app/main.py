from fastapi import FastAPI
from app.api.routes import users, auth, profile, posts
from app.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(profile.router, prefix=settings.API_V1_STR)
app.include_router(posts.router, prefix=settings.API_V1_STR)


# uvicorn app.main:app --reload
# alembic revision --autogenerate -m "create users table"
# alembic upgrade head
