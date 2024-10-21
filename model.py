from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),     server_default=text('now()'))

class Game(Base):
        __tablename__ = "games"
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
        data = Column(JSON, nullable=False)
        answers = Column(JSON, nullable=False)
