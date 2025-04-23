from fastapi import APIRouter, HTTPException
from modelos.lista_vuelos import ListaDoblementeEnlazada
from modelos.modelos import Vuelo, Base
from esquemas.esquema import VueloInput
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List

router = APIRouter()
lista = ListaDoblementeEnlazada()


DATABASE_URL = "sqlite:///./vuelos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@router.post("/vuelos/")
def agregar_vuelo(vuelo: VueloInput):
    db = SessionLocal()
    nuevo_vuelo = Vuelo(codigo=vuelo.codigo, destino=vuelo.destino, estado=vuelo.estado)
    db.add(nuevo_vuelo)
    db.commit()
    db.refresh(nuevo_vuelo)
    db.close()

    if vuelo.estado == "emergencia":
        lista.insertar_al_frente(nuevo_vuelo.dict())
    else:
        lista.insertar_al_final(nuevo_vuelo.dict())
    return {"mensaje": "Vuelo agregado exitosamente"}

@router.get("/vuelos/", response_model=List[dict])
def listar_vuelos():
    vuelos = []
    actual = lista.primero
    while actual:
        vuelos.append(actual.vuelo)
        actual = actual.siguiente
    return vuelos

@router.get("/vuelos/primero")
def vuelo_primero():
    vuelo = lista.obtener_primero()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos")
    return vuelo

@router.get("/vuelos/ultimo")
def vuelo_ultimo():
    vuelo = lista.obtener_ultimo()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos")
    return vuelo

@router.delete("/vuelos/{posicion}")
def eliminar_vuelo(posicion: int):
    try:
        vuelo = lista.extraer_de_posicion(posicion)
        return {"mensaje": "Vuelo eliminado", "vuelo": vuelo}
    except IndexError:
        raise HTTPException(status_code=404, detail="Posición inválida")

@router.post("/vuelos/posicion/{posicion}")
def insertar_en_posicion(vuelo: VueloInput, posicion: int):
    try:
        nuevo_vuelo = Vuelo(codigo=vuelo.codigo, destino=vuelo.destino, estado=vuelo.estado)
        lista.insertar_en_posicion(nuevo_vuelo.dict(), posicion)
        return {"mensaje": "Vuelo insertado en la posición", "posicion": posicion}
    except IndexError:
        raise HTTPException(status_code=404, detail="Posición inválida")

@router.patch("/vuelos/reordenar")
def reordenar_vuelos(orden: List[int]):
    """ Reordena los vuelos en la cola según el orden proporcionado por el cliente """
    if len(orden) != lista.longitud():
        raise HTTPException(status_code=400, detail="El número de posiciones no coincide con el número de vuelos")

    vuelos_reordenados = []
    actual = lista.primero
    while actual:
        vuelos_reordenados.append(actual.vuelo)
        actual = actual.siguiente

    vuelos_reordenados_ordenados = [vuelos_reordenados[i] for i in orden]

    lista = ListaDoblementeEnlazada()
    for vuelo in vuelos_reordenados_ordenados:
        lista.insertar_al_final(vuelo)

    return {"mensaje": "Vuelos reordenados exitosamente", "vuelos_reordenados": vuelos_reordenados_ordenados}
