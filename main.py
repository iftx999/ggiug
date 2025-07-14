from fastapi import FastAPI
from controller import (
    projeto_controller,
    conexao_controller,
    validacao_controller,
    versao_validacao_controller
)
from database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Rotas
app.include_router(projeto_controller.router)
app.include_router(conexao_controller.router)
app.include_router(validacao_controller.router)
app.include_router(versao_validacao_controller.router)
