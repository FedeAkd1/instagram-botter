from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend.database import engine, get_db, Base
from backend import models, schemas

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM System", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== RUTAS PARA SERVIR FRONTEND ====================
@app.get("/")
async def read_root():
    return FileResponse("frontend/index.html")

@app.get("/clientes")
async def read_clientes_page():
    return FileResponse("frontend/clientes.html")

@app.get("/oportunidades")
async def read_oportunidades_page():
    return FileResponse("frontend/oportunidades.html")

@app.get("/actividades")
async def read_actividades_page():
    return FileResponse("frontend/actividades.html")

# ==================== ENDPOINTS API - CLIENTES ====================
@app.post("/api/clientes/", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    db_cliente = db.query(models.Cliente).filter(models.Cliente.email == cliente.email).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.get("/api/clientes/", response_model=List[schemas.Cliente])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes

@app.get("/api/clientes/{cliente_id}", response_model=schemas.Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.put("/api/clientes/{cliente_id}", response_model=schemas.Cliente)
def actualizar_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    update_data = cliente.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.delete("/api/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(db_cliente)
    db.commit()
    return None

@app.get("/api/clientes/buscar/{termino}", response_model=List[schemas.Cliente])
def buscar_clientes(termino: str, db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).filter(
        (models.Cliente.nombre.contains(termino)) |
        (models.Cliente.empresa.contains(termino)) |
        (models.Cliente.email.contains(termino))
    ).all()
    return clientes

# ==================== ENDPOINTS API - CONTACTOS ====================
@app.post("/api/contactos/", response_model=schemas.Contacto, status_code=status.HTTP_201_CREATED)
def crear_contacto(contacto: schemas.ContactoCreate, db: Session = Depends(get_db)):
    db_contacto = models.Contacto(**contacto.model_dump())
    db.add(db_contacto)
    db.commit()
    db.refresh(db_contacto)
    return db_contacto

@app.get("/api/contactos/", response_model=List[schemas.Contacto])
def listar_contactos(db: Session = Depends(get_db)):
    contactos = db.query(models.Contacto).all()
    return contactos

@app.get("/api/contactos/cliente/{cliente_id}", response_model=List[schemas.Contacto])
def listar_contactos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    contactos = db.query(models.Contacto).filter(models.Contacto.cliente_id == cliente_id).all()
    return contactos

@app.delete("/api/contactos/{contacto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contacto(contacto_id: int, db: Session = Depends(get_db)):
    db_contacto = db.query(models.Contacto).filter(models.Contacto.id == contacto_id).first()
    if db_contacto is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    
    db.delete(db_contacto)
    db.commit()
    return None

# ==================== ENDPOINTS API - OPORTUNIDADES ====================
@app.post("/api/oportunidades/", response_model=schemas.Oportunidad, status_code=status.HTTP_201_CREATED)
def crear_oportunidad(oportunidad: schemas.OportunidadCreate, db: Session = Depends(get_db)):
    db_oportunidad = models.Oportunidad(**oportunidad.model_dump())
    db.add(db_oportunidad)
    db.commit()
    db.refresh(db_oportunidad)
    return db_oportunidad

@app.get("/api/oportunidades/", response_model=List[schemas.Oportunidad])
def listar_oportunidades(db: Session = Depends(get_db)):
    oportunidades = db.query(models.Oportunidad).all()
    return oportunidades

@app.get("/api/oportunidades/{oportunidad_id}", response_model=schemas.Oportunidad)
def obtener_oportunidad(oportunidad_id: int, db: Session = Depends(get_db)):
    oportunidad = db.query(models.Oportunidad).filter(models.Oportunidad.id == oportunidad_id).first()
    if oportunidad is None:
        raise HTTPException(status_code=404, detail="Oportunidad no encontrada")
    return oportunidad

@app.put("/api/oportunidades/{oportunidad_id}", response_model=schemas.Oportunidad)
def actualizar_oportunidad(oportunidad_id: int, oportunidad: schemas.OportunidadUpdate, db: Session = Depends(get_db)):
    db_oportunidad = db.query(models.Oportunidad).filter(models.Oportunidad.id == oportunidad_id).first()
    if db_oportunidad is None:
        raise HTTPException(status_code=404, detail="Oportunidad no encontrada")
    
    update_data = oportunidad.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_oportunidad, key, value)
    
    db.commit()
    db.refresh(db_oportunidad)
    return db_oportunidad

@app.delete("/api/oportunidades/{oportunidad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_oportunidad(oportunidad_id: int, db: Session = Depends(get_db)):
    db_oportunidad = db.query(models.Oportunidad).filter(models.Oportunidad.id == oportunidad_id).first()
    if db_oportunidad is None:
        raise HTTPException(status_code=404, detail="Oportunidad no encontrada")
    
    db.delete(db_oportunidad)
    db.commit()
    return None

# ==================== ENDPOINTS API - ACTIVIDADES ====================
@app.post("/api/actividades/", response_model=schemas.Actividad, status_code=status.HTTP_201_CREATED)
def crear_actividad(actividad: schemas.ActividadCreate, db: Session = Depends(get_db)):
    db_actividad = models.Actividad(**actividad.model_dump())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

@app.get("/api/actividades/", response_model=List[schemas.Actividad])
def listar_actividades(db: Session = Depends(get_db)):
    actividades = db.query(models.Actividad).all()
    return actividades

@app.get("/api/actividades/{actividad_id}", response_model=schemas.Actividad)
def obtener_actividad(actividad_id: int, db: Session = Depends(get_db)):
    actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
    if actividad is None:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return actividad

@app.put("/api/actividades/{actividad_id}", response_model=schemas.Actividad)
def actualizar_actividad(actividad_id: int, actividad: schemas.ActividadUpdate, db: Session = Depends(get_db)):
    db_actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
    if db_actividad is None:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    update_data = actividad.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_actividad, key, value)
    
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

@app.delete("/api/actividades/{actividad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_actividad(actividad_id: int, db: Session = Depends(get_db)):
    db_actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
    if db_actividad is None:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    db.delete(db_actividad)
    db.commit()
    return None

# ==================== ENDPOINT DASHBOARD ====================
@app.get("/api/dashboard/estadisticas", response_model=schemas.EstadisticasDashboard)
def obtener_estadisticas(db: Session = Depends(get_db)):
    total_clientes = db.query(models.Cliente).count()
    clientes_activos = db.query(models.Cliente).filter(models.Cliente.estado == "activo").count()
    
    total_oportunidades = db.query(models.Oportunidad).count()
    valor_total = db.query(models.Oportunidad).all()
    valor_total_oportunidades = sum([op.valor for op in valor_total])
    
    oportunidades_ganadas = db.query(models.Oportunidad).filter(models.Oportunidad.etapa == "ganado").count()
    
    actividades_pendientes = db.query(models.Actividad).filter(models.Actividad.completada == False).count()
    
    return {
        "total_clientes": total_clientes,
        "clientes_activos": clientes_activos,
        "total_oportunidades": total_oportunidades,
        "valor_total_oportunidades": valor_total_oportunidades,
        "oportunidades_ganadas": oportunidades_ganadas,
        "actividades_pendientes": actividades_pendientes
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
