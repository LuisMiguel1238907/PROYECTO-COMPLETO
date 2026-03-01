from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# --- USUARIOS ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario (mínimo 3 caracteres)")
    password: str = Field(..., min_length=6, description="La contraseña debe tener al menos 6 caracteres")

# --- CLIENTES ---
class ClientBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nombre completo del cliente")
    dni: str = Field(..., min_length=6, max_length=20, description="Documento de identidad del cliente")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    address: Optional[str] = Field(None, max_length=100, description="Dirección del cliente")

class ClientOut(ClientBase):
    id: int
    class Config:
        from_attributes = True

# --- PRÉSTAMOS ---
class LoanCreate(BaseModel):
    client_id: int
    amount: float = Field(..., gt=0, description="Monto del préstamo (debe ser mayor a 0)")
    interest_rate: float = Field(..., ge=0, le=100, description="Tasa de interés (0-100%)")
    term_days: int = Field(..., gt=0, description="Plazo del préstamo en días")
    start_date: date = Field(..., description="Fecha de inicio del préstamo")

class LoanOut(BaseModel):
    id: int
    client_id: int
    amount: float
    interest_rate: float
    term_days: int
    start_date: date
    end_date: date
    status: str
    class Config:
        from_attributes = True

# --- PAGOS ---
class PaymentCreate(BaseModel):
    loan_id: int
    amount: float = Field(..., gt=0, description="Monto del pago (debe ser mayor a 0)")
    payment_date: date = Field(..., description="Fecha del pago")

class PaymentOut(BaseModel):
    id: int
    loan_id: int
    amount: float
    payment_date: date
    class Config:
        from_attributes = True