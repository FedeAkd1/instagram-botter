from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    empresa = Column(String)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)
    direccion = Column(String)
    estado = Column(String, default="activo")  # activo, inactivo, potencial
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    notas = Column(Text)
    
    contactos = relationship("Contacto", back_populates="cliente", cascade="all, delete-orphan")
    oportunidades = relationship("Oportunidad", back_populates="cliente", cascade="all, delete-orphan")
    actividades = relationship("Actividad", back_populates="cliente", cascade="all, delete-orphan")

class Contacto(Base):
    __tablename__ = "contactos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    cargo = Column(String)
    email = Column(String)
    telefono = Column(String)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    
    cliente = relationship("Cliente", back_populates="contactos")

class Oportunidad(Base):
    __tablename__ = "oportunidades"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(Text)
    valor = Column(Float)
    etapa = Column(String, default="prospecto")  # prospecto, calificado, propuesta, negociacion, ganado, perdido
    probabilidad = Column(Integer, default=10)  # 0-100
    fecha_cierre_estimada = Column(DateTime)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    
    cliente = relationship("Cliente", back_populates="oportunidades")

class Actividad(Base):
    __tablename__ = "actividades"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)  # llamada, email, reunion, tarea
    titulo = Column(String)
    descripcion = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)
    completada = Column(Boolean, default=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    
    cliente = relationship("Cliente", back_populates="actividades")
