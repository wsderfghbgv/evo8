"""Dependencias reutilizables con Depends()."""

from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, status

from app.data import users_db
from app.schemas.user_schema import RoleType

# Configuración general de la API (reto integrador / demo)
API_CONFIG = {
    "app_name": "device_systems",
    "max_users_hint": 1000,
    "default_page_size": 50,
}


def get_api_config() -> dict:
    """Retorna configuración general de la API."""
    return API_CONFIG


def validate_role(role: str) -> str:
    """Valida que el rol esté permitido."""
    if role not in users_db.ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no permitido. Roles válidos: {', '.join(users_db.ALLOWED_ROLES)}",
        )
    return role


def validate_email_unique(
    email: str,
    exclude_id: Optional[int] = None,
) -> str:
    """Valida que el correo no esté registrado."""
    if users_db.email_exists(email, exclude_id=exclude_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )
    return email


def get_user_or_404(user_id: int) -> dict:
    """Obtiene un usuario por ID o lanza 404."""
    user = users_db.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


def verify_api_key(
    x_api_key: Annotated[
        Optional[str],
        Header(alias="X-API-Key", description="Clave opcional para simular autenticación"),
    ] = None,
) -> Optional[str]:
    """
    Simula autenticación básica mediante cabecera.
    No bloquea la petición; solo valida formato si se envía.
    """
    if x_api_key is not None and len(x_api_key.strip()) < 8:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida (mínimo 8 caracteres)",
        )
    return x_api_key


# Tipos anotados para inyección en rutas
UserDep = Annotated[dict, Depends(get_user_or_404)]
ApiConfigDep = Annotated[dict, Depends(get_api_config)]
ApiKeyDep = Annotated[Optional[str], Depends(verify_api_key)]
