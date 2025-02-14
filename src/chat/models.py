from sqlalchemy import Column, BigInteger, Text, DateTime, Integer, String, Boolean
from database import Base


class ChatAI(Base):
    __tablename__ = "chatais"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Text(collation="utf8mb4_unicode_ci"), nullable=False)
    user_message = Column(Text(collation="utf8mb4_unicode_ci"), nullable=False)
    bot_response = Column(Text(collation="utf8mb4_unicode_ci"), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class ChatWithAI(Base):
    __tablename__ = "chat_with_ais"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    group_discussion_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    comment = Column(
        Text(length=4294967295, collation="utf8mb4_unicode_ci"), nullable=True
    )  # LONGTEXT
    ai_answer = Column(
        Text(length=4294967295, collation="utf8mb4_unicode_ci"), nullable=True
    )  # LONGTEXT
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class ChatAI(Base):
    __tablename__ = "chatais"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    chat_id = Column(Text(collation="utf8mb4_unicode_ci"), nullable=False)
    user_message = Column(Text(collation="utf8mb4_unicode_ci"), nullable=False)
    bot_response = Column(Text(collation="utf8mb4_unicode_ci"), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    chat_id = Column(Integer, nullable=True)
    project_detail_id = Column(Integer, nullable=False)
    project_type = Column(
        Integer, nullable=False, default=1, comment="1 => Focus Group, 2 => Workflow"
    )
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=True)
    video = Column(String(255), nullable=True)
    document = Column(String(255), nullable=True)
    image_1 = Column(String(255), nullable=True)
    image_2 = Column(String(255), nullable=True)
    image_3 = Column(String(255), nullable=True)
    video_size = Column(Integer, nullable=True, comment="Size In KB")
    document_size = Column(Integer, nullable=True, comment="Size In KB")
    image_1_size = Column(Integer, nullable=True, comment="Size In KB")
    image_2_size = Column(Integer, nullable=True, comment="Size In KB")
    image_3_size = Column(Integer, nullable=True, comment="Size In KB")
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
