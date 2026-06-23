"""
Auditoría de mercados de apuestas 1X2: agrupa los cálculos en estructuras
de datos simples, separadas de la UI.
"""

from dataclasses import dataclass
from typing import List, Optional

from core.odds_converter import (
    americana_a_implicita,
    calcular_overround,
    detectar_value_bet,
)


@dataclass
class ResultadoOpcion:
    nombre: str
    cuota: int
    probabilidad_implicita: float


@dataclass
class ResultadoMercado:
    partido: str
    opciones: List[ResultadoOpcion]
    total_probabilidad: float
    margen_casa: float


def auditar_mercado(partido: str, cuotas: dict) -> ResultadoMercado:
    """
    cuotas: dict {nombre_opcion: cuota_americana}
    Ej: {"Local": -150, "Empate": 240, "Visita": 320}
    """
    opciones = [
        ResultadoOpcion(nombre=nombre, cuota=cuota, probabilidad_implicita=americana_a_implicita(cuota))
        for nombre, cuota in cuotas.items()
    ]
    total, margen = calcular_overround([o.probabilidad_implicita for o in opciones])
    return ResultadoMercado(partido=partido, opciones=opciones, total_probabilidad=total, margen_casa=margen)


def evaluar_value_bet(probabilidad_implicita: float, probabilidad_estimada: float) -> Optional[tuple]:
    """Devuelve (es_value, ventaja) usando la lógica del core."""
    return detectar_value_bet(probabilidad_implicita, probabilidad_estimada)


@dataclass
class Recomendacion:
    opcion: Optional[str]
    ventaja: float
    todas: List[dict]


def recomendar_apuesta(resultado: ResultadoMercado, probabilidades_estimadas: dict) -> Recomendacion:
    """
    Compara cada opción del mercado contra una probabilidad real estimada
    (probabilidades_estimadas: {nombre_opcion: probabilidad_estimada}) y
    devuelve la opción con mayor ventaja (+EV), si existe alguna.

    Si ninguna opción tiene valor positivo, opcion=None.
    """
    detalle = []
    for opcion in resultado.opciones:
        prob_estimada = probabilidades_estimadas.get(opcion.nombre, 0.0)
        es_valor, ventaja = detectar_value_bet(opcion.probabilidad_implicita, prob_estimada)
        detalle.append({
            "nombre": opcion.nombre,
            "cuota": opcion.cuota,
            "prob_implicita": opcion.probabilidad_implicita,
            "prob_estimada": prob_estimada,
            "ventaja": ventaja,
            "es_valor": es_valor,
        })

    candidatos = [d for d in detalle if d["es_valor"]]
    if not candidatos:
        return Recomendacion(opcion=None, ventaja=0.0, todas=detalle)

    mejor = max(candidatos, key=lambda d: d["ventaja"])
    return Recomendacion(opcion=mejor["nombre"], ventaja=mejor["ventaja"], todas=detalle)
