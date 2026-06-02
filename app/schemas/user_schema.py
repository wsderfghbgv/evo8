"""Modelos Pydantic v2 para entrada y salida de usuarios."""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

RoleType = Literal["admin", "operator", "support", "viewer"]


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico único")
    role: RoleType = Field(..., description="Rol del usuario en el sistema")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")


class UserCreate(UserBase):
    """Modelo para crear un nuevo usuario."""

    pass


class UserUpdateFull(UserBase):
    """Modelo para actualización completa (PUT). Todos los campos son requeridos."""

    pass


class UserUpdatePartial(BaseModel):
    """Modelo para actualización parcial (PATCH). Todos los campos son opcionales."""

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[RoleType] = None
    is_active: Optional[bool] = None

    def has_updates(self) -> bool:
        return any(
            v is not None
            for v in (self.name, self.email, self.role, self.is_active)
        )


class UserResponse(UserBase):
    """Modelo de respuesta con identificador."""

    id: int = Field(..., description="Identificador único del usuario")

    model_config = ConfigDict(from_attributes=True)


class DeleteMessage(BaseModel):
    message: str
