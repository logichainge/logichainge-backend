from app.database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, text, ARRAY


class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    activity_id = Column(Integer, ForeignKey('activity.id'))
    unit_type = Column(ARRAY(String), nullable=False)
    stackable = Column(Boolean, default=False, nullable=False)
    quantity = Column(ARRAY(String), default="1", nullable=False)
    description = Column(ARRAY(String), nullable=False)
    loading_meters = Column(ARRAY(String), nullable=False)
    net_weight = Column(ARRAY(String), nullable=True)
    gross_weight = Column(ARRAY(String), nullable=False)
    dangerous_goods = Column(Boolean, default=False, nullable=False)
    dg_class = Column(String, nullable=True)
    dg_product_group = Column(String, nullable=True)
    dg_un_code = Column(String, nullable=True)
    dg_technical_name = Column(String, nullable=True)
    
    size = Column(ARRAY(String), nullable=False)
    volume_cbm = Column(ARRAY(String), nullable=False)

    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    