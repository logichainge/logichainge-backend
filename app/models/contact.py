from app.database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ARRAY, ForeignKey


class Contact(Base):
	__tablename__ = "contact"
	
	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	client_id = Column(Integer, ForeignKey('client.id'), nullable = True)
	initials = Column(String, nullable=True)
	name = Column(String, nullable=False)
	surname_prefix = Column(String, nullable=True)
	surname = Column(String, nullable=False)
	phone = Column(ARRAY(String), nullable=True)
	mobile = Column(ARRAY(String), nullable=True)
	email = Column(ARRAY(String), nullable=True)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	# transport_file_id = Column(Integer, ForeignKey('transport_file.id'))






