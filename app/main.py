"""Punto de entrada de la API device_systems."""

from fastapi import FastAPI

from app.routes import user_routes

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema device_systems. "
        "Incluye CRUD completo, manejo de errores, filtros y documentación OpenAPI."
    ),
    version="2.0.0",
    contact={
        "name": "Equipo device_systems",
        "email": "soporte@device-systems.com",
    },
    license_info={
        "name": "Uso académico SENA",
    },
)

app.include_router(user_routes.router)


@app.get("/", tags=["Health"], summary="Estado de la API")
def root():
    return {
        "message": "device_systems API en ejecución",
        "docs": "/docs",
        "redoc": "/redoc",
    }
