from sqlalchemy import Boolean, Column, Integer, Numeric, String, Text, DateTime, BIGINT
from database import Base
from sqlalchemy.sql import func


class Agent(Base):
    __tablename__ = "ai_agents"

    id = Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String(255), unique=True)
    name = Column(String(255), nullable=True)
    cost = Column(Numeric(precision=10, scale=2), nullable=True)
    description = Column(Text, nullable=True)
    profile_image = Column(String(255), nullable=True)
    video = Column(String(255), nullable=True)
    key_feature = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    personality = Column(Text, nullable=True)
    focus_group_survey = Column(String(255), nullable=True)
    own_data = Column(String(255), nullable=True)
    top_idea = Column(String(255), nullable=True)
    api_data = Column(String(255), nullable=True)
    survey = Column(String(255), nullable=True)
    group_id = Column(Text, nullable=True)
    vector_id = Column(String(36), nullable=True)
    # tools = Column(String(255), nullable=True)
    is_chatbot = Column(Boolean, default=False)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )
