from app.database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean
from sqlalchemy.orm import relationship, backref
import uuid

class User(Base):
	__tablename__ = "user"
	
	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	username = Column(String, nullable=False)
	email = Column(String, nullable=False)
	full_name = Column(String, nullable=False)
	disabled = Column(Boolean, nullable = False)
	first_login = Column(Boolean, nullable = True)
	password_reset_needed = Column(Boolean, nullable = True)
	is_admin = Column(Boolean, nullable = True)
	hashed_pass = Column(String, nullable = False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))