from pydantic import BaseModel


class ProfileBase(BaseModel):
    bio: str = None
    avatar_url: str = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True
