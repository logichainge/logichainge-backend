from app.database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey


class Department(Base):
	__tablename__ = "department"
	
	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	client_id = Column(Integer, ForeignKey('client.id'), nullable = True)
	name = Column(String, nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	# transport_file_id = Column(Integer, ForeignKey('transport_file.id'))
