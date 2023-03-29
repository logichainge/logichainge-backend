from app.database.database import Base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, text, ARRAY


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(ARRAY(String), nullable=False)
    street_1 = Column(ARRAY(String), nullable=False)
    street_2 = Column(ARRAY(String), nullable=True)
    street_3 = Column(ARRAY(String), nullable=True)
    zipcode = Column(ARRAY(String), nullable=False)
    city = Column(ARRAY(String), nullable=True, server_default=text("'Example_city'"))
    country = Column(ARRAY(String), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
