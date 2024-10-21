from pydantic import BaseModel


class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    class Config:
        orm_mode = True

class CreateGame(PostBase):
    score: int
    
    class Config:
        orm_mode = True


class GameData(BaseModel):
    data: dict
    answers: list