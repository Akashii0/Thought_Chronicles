from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    author = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))
    profile_picture = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", backref="blogs")

class Like(Base):
    __tablename__ = "likes"
    # id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    blog_id = Column(Integer, ForeignKey(
        "blogs.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))

    __table_args__ = (UniqueConstraint("user_id", "blog_id", name="user_blog_unique"),)
