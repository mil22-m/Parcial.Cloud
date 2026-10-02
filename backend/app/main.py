from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, videos #comments

# Crea las tablas automáticamente en la base de datos (PostgreSQL o SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Video Platform API",
    description="API RESTful para la plataforma de videos con soporte AWS S3 y RDS",
    version="1.0.0",
    docs_url="/docs"
)

# Permitir solicitudes desde el Frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar routers
app.include_router(auth.router)
app.include_router(videos.router)
#app.include_router(comments.router)

@app.get("/")
def root():
    return {"message": "API de la Plataforma de Videos activa. Visita /docs para la documentación."}