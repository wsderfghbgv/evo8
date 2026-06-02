"""Definición de endpoints del recurso /users."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response, status

from app.dependencies.user_dependencies import ApiConfigDep, ApiKeyDep, UserDep
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdateFull,
    UserUpdatePartial,
)
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Obtiene todos los usuarios. Permite filtrar por rol y estado activo.",
    response_description="Lista de usuarios registrados",
)
def list_users(
    _config: ApiConfigDep,
    _api_key: ApiKeyDep,
    role: Optional[str] = Query(
        None,
        description="Filtrar por rol: admin, operator, support, viewer",
    ),
    is_active: Optional[bool] = Query(
        None,
        description="Filtrar por estado activo (true/false)",
    ),
):
    return user_service.list_users(role=role, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Retorna un usuario específico según su identificador.",
    response_description="Usuario encontrado",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_user_by_id(user: UserDep):
    return UserResponse(**user)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario en el sistema.",
    response_description="Usuario creado correctamente",
    responses={
        400: {"description": "Correo duplicado o rol no permitido"},
        422: {"description": "Datos de entrada inválidos"},
    },
)
def create_user(
    payload: UserCreate,
    _api_key: ApiKeyDep,
):
    return user_service.create_user(payload)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario (completo)",
    description="Reemplaza por completo la información del usuario. Todos los campos son obligatorios.",
    response_description="Usuario actualizado",
    responses={
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Correo duplicado o rol no permitido"},
    },
)
def update_user_full(user_id: int, payload: UserUpdateFull, user: UserDep):
    return user_service.replace_user(user_id, payload)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario (parcial)",
    description="Modifica solo los campos enviados en el cuerpo de la petición.",
    response_description="Usuario actualizado parcialmente",
    responses={
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Sin campos para actualizar, correo duplicado o rol inválido"},
    },
)
def update_user_partial(user_id: int, payload: UserUpdatePartial, user: UserDep):
    return user_service.patch_user(user_id, payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema. No retorna cuerpo en la respuesta.",
    response_description="Usuario eliminado sin contenido en el cuerpo",
    responses={404: {"description": "Usuario no encontrado"}},
)
def remove_user(user_id: int, user: UserDep):
    user_service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
