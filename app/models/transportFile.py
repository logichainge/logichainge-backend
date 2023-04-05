from app.database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, text, ARRAY, Numeric
from sqlalchemy.orm import relationship, backref

class TransportFile(Base):
    __tablename__ = "transport_file"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    activity = relationship('Activity', cascade = "all, delete-orphan")
    tr_file_status = Column(String, nullable=True, server_default="pending")  # Can be converted to ENUM
    display_number = Column(String, nullable=True)
    invoice_reference = Column(ARRAY(String), nullable=True)
    file_type = Column(String, nullable=True)
    equipment_type = Column(String, nullable=True)
    modality = Column(String, nullable=True)  # Can be converted to ENUM
    service_level = Column(String, nullable=True)
    customs = Column(String, nullable=True)
    attention_required = Column(Boolean, nullable=True)
    multi_trip = Column(Boolean, nullable=True, server_default="False", default=False)
    multi_activity = Column(Boolean, nullable=True, server_default="False", default=False)
    date_deviation = Column(Boolean, nullable=True, server_default="False", default=False)
    urgency = Column(Boolean, nullable=True, server_default="False", default=False)
    late_booking = Column(Boolean, nullable=True, server_default="False", default=False)
    cost_code = Column(String, nullable=True)
    
    client_id = Column(Integer, ForeignKey('client.id'), nullable = True)
    client = relationship('Client')
    
    contact_id = Column(Integer, ForeignKey('contact.id'), nullable = True)
    contact = relationship('Contact')   
    
    department_id = Column(Integer, ForeignKey('department.id'), nullable = True)
    department = relationship('Department')
    
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable = True)
    employee = relationship('Employee')
    reported = Column(Boolean, nullable=True, server_default="False", default=False)
    call_before_planning = Column(Boolean, nullable=True, server_default="False", default=False)
    incoterms = Column(String, nullable=True)
    certainty = Column(Integer, nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    reference = Column(ARRAY(String), nullable=True) #list of urls
    accuracy = Column(Numeric, nullable = True)


    