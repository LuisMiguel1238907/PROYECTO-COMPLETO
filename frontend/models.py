from sqlalchemy import Column, Integer, String, DECIMAL, Date, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    dni = Column(String(30), unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(String(255))

    loans = relationship("Loan", back_populates="client")

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    interest_rate = Column(DECIMAL(5,2), nullable=False)
    term_days = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum('pendiente','pagado','vencido'), default='pendiente')
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    client = relationship("Client", back_populates="loans")
    payments = relationship("Payment", back_populates="loan")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    payment_date = Column(Date, nullable=False)

    loan = relationship("Loan", back_populates="payments")