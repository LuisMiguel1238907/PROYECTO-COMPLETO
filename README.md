# Sistema de Préstamos – Proyecto Completo

Este proyecto es un sistema de gestión de préstamos, con backend en **FastAPI + MySQL** y frontend en **HTML, CSS y JavaScript**.  
Incluye manejo de clientes, préstamos, pagos, reportes en Excel y PDF, autenticación con JWT y panel administrativo.

---

## 📁 Estructura del Proyecto
PROYECTOCOMPLETO/
│
├── Backend/
│ ├── routers/
│ ├── venv/
│ ├── auth.py
│ ├── crud.py
│ ├── database.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── utils.py
│ ├── requirements.txt
│ └── (archivos de reportes PDF/Excel)
│
└── Frontend/
├── index.html
├── css/
├── js/
└── (otros archivos)



---

## ⚙️ Instalación del Backend (FastAPI)

1. Entrar al directorio:

```bash
cd backend

#Crear entorno virtual
python -m venv venv

#Activar Entorno
venv\Scripts\activate

#Dependencias: 
pip install -r requirements.txt

#uvicorn main:app --reload


#Base de Datos

#Este proyecto usa MySQL.

#Crear la base de datos:

#CREATE DATABASE backend_db;

#Asegurar que el usuario y contraseña coinciden con database.py.

#FastAPI creará las tablas automáticamente al iniciar.

#🎨 Frontend (HTML + CSS + JS)

#Para ejecutar el frontend:

#Abrir la carpeta Frontend/ en VS Code.

#Usar la extensión Live Server o abrir el archivo index.html directamente.

#El frontend consume los endpoints del backend mediante peticiones fetch.

#🔐 Autenticación

#El sistema usa:

#JWT (tokens)

#Login mediante /login

#Protección de rutas en backend

#📊 Reportes

#El módulo de reportes permite:

#Descargar Excel con openpyxl

#Descargar PDF con reportlab

#🤝 Colaboración en Equipo

#Para que cualquier miembro del equipo instale el backend:

#git clone <repo>
#cd Backend
#python -m venv venv
#venv\Scripts\activate
#pip install -r requirements.txt
#uvicorn main:app --reload