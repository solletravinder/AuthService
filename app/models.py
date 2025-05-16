from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from .database import Base
from datetime import datetime

# Association table for chat rooms and users
chat_room_users = Table(
    'chat_room_users',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('chat_room_id', Integer, ForeignKey('chat_rooms.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    messages_sent = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    chat_rooms = relationship("ChatRoom", secondary=chat_room_users, back_populates="users")

class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # Can be null for direct messages
    is_group = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationships
    users = relationship("User", secondary=chat_room_users, back_populates="chat_rooms")
    messages = relationship("Message", back_populates="chat_room")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    content = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationships
    sender = relationship("User", back_populates="messages_sent", foreign_keys=[sender_id])
    chat_room = relationship("ChatRoom", back_populates="messages")
