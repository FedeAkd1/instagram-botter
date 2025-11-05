from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Schemas para Cliente
class ClienteBase(BaseModel):
    nombre: str
    empresa: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[str] = "activo"
    notas: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    empresa: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[str] = None
    notas: Optional[str] = None

class Cliente(ClienteBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

# Schemas para Contacto
class ContactoBase(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    cliente_id: int

class ContactoCreate(ContactoBase):
    pass

class Contacto(ContactoBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Oportunidad
class OportunidadBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    valor: float
    etapa: Optional[str] = "prospecto"
    probabilidad: Optional[int] = 10
    fecha_cierre_estimada: Optional[datetime] = None
    cliente_id: int

class OportunidadCreate(OportunidadBase):
    pass

class OportunidadUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    valor: Optional[float] = None
    etapa: Optional[str] = None
    probabilidad: Optional[int] = None
    fecha_cierre_estimada: Optional[datetime] = None

class Oportunidad(OportunidadBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

# Schemas para Actividad
class ActividadBase(BaseModel):
    tipo: str
    titulo: str
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None
    completada: Optional[bool] = False
    cliente_id: int

class ActividadCreate(ActividadBase):
    pass

class ActividadUpdate(BaseModel):
    tipo: Optional[str] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None
    completada: Optional[bool] = None

class Actividad(ActividadBase):
    id: int
    
    class Config:
        from_attributes = True

# Schema para estadísticas del dashboard
class EstadisticasDashboard(BaseModel):
    total_clientes: int
    clientes_activos: int
    total_oportunidades: int
    valor_total_oportunidades: float
    oportunidades_ganadas: int
    actividades_pendientes: int
