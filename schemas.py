from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):   # shared between returning and creating a post
    title: str = Field(min_length=1, max_length=100)   # after = are constraints
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)


# Defines what we accept when creating a new post
class PostCreate(PostBase):
    pass


#Defines what we return from API
class PostResponse(PostBase):  # PostResponse inherits title, content and author from PostBase; adding id and date_posted.
    model_config = ConfigDict(from_attributes=True) # this tells pydantic that it can read data from object with attributes not just dictionaries
    
    # fields that we want in our response not provided by client
    id: int
    date_posted: str