from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import HTTPException, status
import models
import schemas

# ---------- USERS ----------
def create_user(db: Session, username: str, password: str):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe"
        )
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---------- CLIENTS ----------
def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

def get_client_by_id(db: Session, client_id: int):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

def create_client(db: Session, client: schemas.ClientBase):
    existing_client = db.query(models.Client).filter(models.Client.dni == client.dni).first()
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con este DNI"
        )
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# ---------- LOANS ----------
def create_loan(db: Session, loan: schemas.LoanCreate, created_by: int):
    client = db.query(models.Client).filter(models.Client.id == loan.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    end_date = loan.start_date + timedelta(days=loan.term_days)
    
    db_loan = models.Loan(
        client_id=loan.client_id,
        amount=loan.amount,
        interest_rate=loan.interest_rate,
        term_days=loan.term_days,
        start_date=loan.start_date,
        end_date=end_date,
        created_by=created_by,
        status="Activo"
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_loans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Loan).offset(skip).limit(limit).all()

def get_loan_by_id(db: Session, loan_id: int):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan

# ---------- PAYMENTS ----------
def create_payment(db: Session, payment: schemas.PaymentCreate):
    loan = db.query(models.Loan).filter(models.Loan.id == payment.loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    # Verificar si ya se pagó completamente el préstamo
    total_paid = sum(p.amount for p in db.query(models.Payment).filter(models.Payment.loan_id == payment.loan_id))
    total_due = loan.amount + (loan.amount * loan.interest_rate / 100)
    if total_paid >= total_due:
        loan.status = "Pagado"
        db.commit()

    return db_payment

def get_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Payment).offset(skip).limit(limit).all()