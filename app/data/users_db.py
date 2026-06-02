"""Simulación de base de datos en memoria para usuarios."""

from typing import Dict, List, Optional

# Roles permitidos en el sistema
ALLOWED_ROLES = ("admin", "operator", "support", "viewer")

# Almacén en memoria: user_id -> dict
_users: Dict[int, dict] = {}
_next_id: int = 1


def _seed_data() -> None:
    """Carga usuarios de ejemplo al iniciar."""
    global _next_id
    samples = [
        {
            "name": "Ana García",
            "email": "ana.garcia@device.com",
            "role": "admin",
            "is_active": True,
        },
        {
            "name": "Carlos López",
            "email": "carlos.lopez@device.com",
            "role": "operator",
            "is_active": True,
        },
        {
            "name": "María Ruiz",
            "email": "maria.ruiz@device.com",
            "role": "support",
            "is_active": False,
        },
    ]
    for user in samples:
        _users[_next_id] = {"id": _next_id, **user}
        _next_id += 1


_seed_data()


def get_all_users() -> List[dict]:
    return list(_users.values())


def get_user_by_id(user_id: int) -> Optional[dict]:
    return _users.get(user_id)


def email_exists(email: str, exclude_id: Optional[int] = None) -> bool:
    email_lower = email.lower()
    for uid, user in _users.items():
        if exclude_id is not None and uid == exclude_id:
            continue
        if user["email"].lower() == email_lower:
            return True
    return False


def create_user(data: dict) -> dict:
    global _next_id
    user = {"id": _next_id, **data}
    _users[_next_id] = user
    _next_id += 1
    return user


def replace_user(user_id: int, data: dict) -> dict:
    user = {"id": user_id, **data}
    _users[user_id] = user
    return user


def update_user_partial(user_id: int, updates: dict) -> dict:
    user = _users[user_id].copy()
    user.update(updates)
    _users[user_id] = user
    return user


def delete_user(user_id: int) -> bool:
    if user_id not in _users:
        return False
    del _users[user_id]
    return True
