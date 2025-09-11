from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import (
    projeto_controller,
    conexao_controller,
    validacao_controller,
    versao_validacao_controller,
    medicao_controller

)
from database import Base, engine

app = FastAPI()

# ADICIONE ISSO AQUI ANTES DE TUDO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ CORS configurado")

Base.metadata.create_all(bind=engine)

# Rotas
app.include_router(projeto_controller.router)
app.include_router(conexao_controller.router)
app.include_router(validacao_controller.router)
app.include_router(versao_validacao_controller.router)
app.include_router(medicao_controller.router)



