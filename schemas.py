from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel): # whats shared between UserCreate and UserResponse
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)

class UserCreate(UserBase):
    pass
    

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    image_file: str | None
    image_path: str # property on user model


class PostBase(BaseModel):   # shared between returning and creating a post
    title: str = Field(min_length=1, max_length=100)   # after = are constraints
    content: str = Field(min_length=1)


# Defines what we accept when creating a new post
class PostCreate(PostBase):
    user_id: int # TEMPORARY: will be replaced with current user from session


#Defines what we return from API
class PostResponse(PostBase):  # PostResponse inherits title, content and author from PostBase; adding id and date_posted.
    model_config = ConfigDict(from_attributes=True) # this tells pydantic that it can read data from object with attributes not just dictionaries
    
    # fields that we want in our response not provided by client
    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse