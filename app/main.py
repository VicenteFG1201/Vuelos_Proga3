from app.rutas import router
from fastapi import FastAPI

app = FastAPI(title="Gestión de Vuelos con Lista Doblemente Enlazada")

# Incluyendo las rutas del archivo rutas.py
app.include_router(router)

# Ruta raíz con mensaje de bienvenida
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de gestión de vuelos"}
