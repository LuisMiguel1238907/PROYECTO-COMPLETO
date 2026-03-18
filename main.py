from fastapi import FastAPI
from fastapi.responses import FileResponse
import os # Importamos os para una mejor gestión de archivos (aunque no lo uses aquí, es buena práctica)

app = FastAPI()

# 1. RUTA PRINCIPAL: Página de Bienvenida
# Sirve el contenido del archivo 'index.html'
@app.get("/")
def serve_welcome():
    return FileResponse("index.html")

# 2. RUTA DE INICIO DE SESIÓN
# Nota: Si tu botón de bienvenida apunta a "/login", deberías usar esa ruta aquí.
# Si estás usando esta ruta para el dashboard (como en tu código anterior), 
# es importante que refleje el nombre del archivo.

@app.get("/dashboard")
def serve_dashboard():
    # Sirve el contenido del archivo 'index2.html' (el dashboard)
    return FileResponse("index2.html")

# 3. RUTA DE RECUPERACIÓN DE CONTRASEÑA
# Cambié el nombre de la función a 'serve_forgot_password' para evitar duplicados.
# También corregí el nombre del archivo de retorno a "olvidarcontrasenia.html", 
# que es el que usamos en el último ejercicio, asumiendo que es el nombre correcto.

@app.get("/olvidocontrasena")
def serve_forgot_password():
    # Sirve el contenido del archivo 'olvidarcontrasenia.html'
    return FileResponse("olvidarcontrasenia.html")from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routers import reports



from database import engine
from models import Base

# ✅ Importar Routers
from routers.auth_routes import router as auth_router
from routers import clients, loans, payments, dashboard_routes
# from routers import reports  # <-- Si tienes reports, descomenta

# ✅ Crear la app
app = FastAPI(
    title="API de Clientes",
    version="1.0"
)

# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Crear tablas
Base.metadata.create_all(bind=engine)

# ✅ Swagger + JWT
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API de Clientes",
        version="1.0.0",
        description="API con autenticación JWT",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ✅ REGISTRO DE RUTAS
app.include_router(auth_router)
app.include_router(clients.router)
app.include_router(loans.router)
app.include_router(payments.router)
app.include_router(dashboard_routes.router)
app.include_router(reports.router)

# ✅ Si tienes reports, solo así:
# app.include_router(reports.router)

# ✅ Ruta principal
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando ✅"}

