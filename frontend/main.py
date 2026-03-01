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
    return FileResponse("olvidarcontrasenia.html")