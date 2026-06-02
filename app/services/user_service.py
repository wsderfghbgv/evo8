"""Lógica de negocio del recurso users."""

from typing import List, Optional

from fastapi import HTTPException, status

from app.data import users_db
from app.dependencies.user_dependencies import validate_email_unique, validate_role
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdateFull,
    UserUpdatePartial,
)


def list_users(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> List[UserResponse]:
    """Lista usuarios con filtros opcionales por rol y estado."""
    users = users_db.get_all_users()
    if role is not None:
        validate_role(role)
        users = [u for u in users if u["role"] == role]
    if is_active is not None:
        users = [u for u in users if u["is_active"] is is_active]
    return [UserResponse(**u) for u in users]


def get_user(user_id: int) -> UserResponse:
    user = users_db.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return UserResponse(**user)


def create_user(payload: UserCreate) -> UserResponse:
    validate_role(payload.role)
    validate_email_unique(payload.email)
    data = payload.model_dump()
    user = users_db.create_user(data)
    return UserResponse(**user)


def replace_user(user_id: int, payload: UserUpdateFull) -> UserResponse:
    if users_db.get_user_by_id(user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    validate_role(payload.role)
    validate_email_unique(payload.email, exclude_id=user_id)
    data = payload.model_dump()
    user = users_db.replace_user(user_id, data)
    return UserResponse(**user)


def patch_user(user_id: int, payload: UserUpdatePartial) -> UserResponse:
    if users_db.get_user_by_id(user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    if not payload.has_updates():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar",
        )

    updates = payload.model_dump(exclude_unset=True)
    if "role" in updates:
        validate_role(updates["role"])
    if "email" in updates:
        validate_email_unique(updates["email"], exclude_id=user_id)

    user = users_db.update_user_partial(user_id, updates)
    return UserResponse(**user)


def delete_user(user_id: int) -> None:
    if not users_db.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
