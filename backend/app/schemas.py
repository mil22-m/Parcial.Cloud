from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Esquema para recibir los datos de Registro desde el Frontend
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Esquema para recibir los datos de Login desde el Frontend
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para responder con la información del usuario (sin devolver la contraseña)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

# Esquema para respuestas de video (usado en el perfil)
class VideoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    views: int
    user_id: int
    user_name: str

    class Config:
        from_attributes = True

# Esquema para el perfil completo de usuario
class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    video_count: int
    videos: List[VideoResponse] = []

    class Config:
        from_attributes = True


# Esquema para ver el detalle de un video específico
class VideoDetailResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    views: int
    user_id: int
    user_name: str

    class Config:
        from_attributes = True