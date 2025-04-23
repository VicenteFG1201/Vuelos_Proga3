from pydantic import BaseModel

class VueloInput(BaseModel):
    codigo: str
    destino: str
    estado: str  # emergencia o regular
