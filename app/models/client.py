from app.database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ARRAY
from sqlalchemy.orm import relationship, backref
import uuid

class Client(Base):
	__tablename__ = "client"
	
	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	contact = relationship('Contact', backref = backref('Contact', cascade = "all, delete"))
	department = relationship('Department', backref = backref('Department', cascade = "all, delete"))
	employee = relationship('Employee', backref = backref('Employee', cascade = "all, delete"))
	client_identifier = Column(String, nullable=False)
	name = Column(ARRAY(String), nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
