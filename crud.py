from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from datetime import date, timedelta
from models import Cliente, Prestamo, Pago
import schemas


# ✅ CREAR CLIENTE
def crear_cliente(db: Session, cliente: schemas.ClienteCreate):
    nuevo_cliente = Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


# ✅ LISTAR CLIENTES
def obtener_clientes(db: Session):
    return db.query(Cliente).all()


# ✅ OBTENER CLIENTE POR ID
def obtener_cliente_por_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


# ✅ CREAR PRÉSTAMO (permite varios)
def crear_prestamo(db: Session, prestamo: schemas.PrestamoCreate):

    # ✅ Verificar cliente
    cliente = obtener_cliente_por_id(db, prestamo.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no existe")

    # ✅ Validaciones lógicas
    if prestamo.monto_inicial <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0")

    total_interes = prestamo.total_interes or 0
    if total_interes < 0:
        raise HTTPException(status_code=400, detail="El interés no puede ser negativo")

    # ✅ Convertir fechas del frontend ('' → None)
    fecha_inicio = prestamo.fecha_inicio or date.today()
    fecha_limite = prestamo.fecha_limite or (fecha_inicio + timedelta(days=30))

    nuevo_prestamo = Prestamo(
        cliente_id=prestamo.cliente_id,
        monto_inicial=prestamo.monto_inicial,
        total_interes=total_interes,
        fecha_inicio=fecha_inicio,
        fecha_limite=fecha_limite,
        monto_pagado=0,
        monto_restante=prestamo.monto_inicial + total_interes,
        estado="Activo"
    )

    db.add(nuevo_prestamo)
    db.commit()
    db.refresh(nuevo_prestamo)
    return nuevo_prestamo


# ✅ LISTAR PRÉSTAMOS (con nombre del cliente)
def listar_prestamos(db: Session):
    return (
        db.query(Prestamo)
        .options(joinedload(Prestamo.cliente))
        .all()
    )


# ✅ OBTENER PRÉSTAMO POR ID
def obtener_prestamo(db: Session, prestamo_id: int):
    return (
        db.query(Prestamo)
        .options(joinedload(Prestamo.cliente))
        .filter(Prestamo.id == prestamo_id)
        .first()
    )


# ✅ ACTUALIZAR PRÉSTAMO
def actualizar_prestamo(db: Session, prestamo_id: int, data: schemas.PrestamoUpdate):
    prestamo = obtener_prestamo(db, prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # ✅ Aplicar solo los campos enviados
    for key, value in data.dict(exclude_unset=True).items():
        if value == "":
            value = None  # evita error si frontend envía string vacío
        setattr(prestamo, key, value)

    db.commit()
    db.refresh(prestamo)
    return prestamo


# ✅ ELIMINAR PRÉSTAMO
def eliminar_prestamo(db: Session, prestamo_id: int):
    prestamo = obtener_prestamo(db, prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    db.delete(prestamo)
    db.commit()
    return {"mensaje": "Préstamo eliminado exitosamente"}


# ✅ LISTAR PAGOS (con datos del cliente y préstamo)
def listar_pagos(db: Session):
    return (
        db.query(Pago)
        .options(
            joinedload(Pago.cliente),
            joinedload(Pago.prestamo)
        )
        .all()
    )

# ✅ CREAR PAGO
def crear_pago(db: Session, pago: schemas.PagoCreate):

    cliente = obtener_cliente_por_id(db, pago.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    prestamo = obtener_prestamo(db, pago.prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    if pago.monto_pagado <= 0:
        raise HTTPException(status_code=400, detail="El monto pagado debe ser mayor a 0")

    if prestamo.estado == "Pagado":
        raise HTTPException(status_code=400, detail="Este préstamo ya está pagado")

    # 🔒 Asegura que el préstamo tenga valores válidos
    total_prestamo = float(prestamo.monto_inicial + prestamo.total_interes)
    if prestamo.monto_restante is None:
        # si por algún motivo no estaba calculado, lo recalculamos
        prestamo.monto_pagado = float(prestamo.monto_pagado or 0)
        prestamo.monto_restante = round(total_prestamo - prestamo.monto_pagado, 2)

    # ✅ Validación contra saldo (con redondeo para evitar errores por decimales)
    saldo = round(float(prestamo.monto_restante), 2)
    monto = round(float(pago.monto_pagado), 2)

    if monto > saldo:
        raise HTTPException(
            status_code=400,
            detail=f"El pago supera el saldo restante. Saldo: {saldo}"
        )

    fecha_pago = pago.fecha_pago or date.today()

    nuevo_pago = Pago(
        cliente_id=pago.cliente_id,
        prestamo_id=pago.prestamo_id,
        monto_pagado=monto,
        fecha_pago=fecha_pago,
        estado=pago.estado,  # si quieres, puedes forzarlo a "Completado"/"Pagado"
    )

    db.add(nuevo_pago)


    # ✅ ACTUALIZAR PRESTAMO
    prestamo.monto_pagado = round(float(prestamo.monto_pagado or 0) + monto, 2)
    prestamo.monto_restante = round(total_prestamo - float(prestamo.monto_pagado), 2)

    if prestamo.monto_restante <= 0:
        prestamo.monto_restante = 0.0
        prestamo.estado = "Pagado"
    else:
        # si no manejas "Atrasado" aquí, déjalo como "Activo"
        if prestamo.estado != "Atrasado":
            prestamo.estado = "Activo"

    db.commit()
    db.refresh(nuevo_pago)
    db.refresh(prestamo)

    return nuevo_pago
