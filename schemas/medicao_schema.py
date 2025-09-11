from pydantic import BaseModel

class MedicaoBase(BaseModel):
    volmedido: int | None = None  # pode ser opcional ou obrigatório

class MedicaoCreate(MedicaoBase):
    pass  # pode usar no POST

class MedicaoResponse(MedicaoBase):
    id: int

    class Config:
        from_attributes = True  # substitui o antigo orm_mode
