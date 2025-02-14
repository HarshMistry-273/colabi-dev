from database import Base
from sqlalchemy import Column, BigInteger, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship


class UserAttribute(Base):
    __tablename__ = 'user_attributes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    attributes = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    