"""
Conversión de cuotas americanas a probabilidad implícita
y cálculo del margen de la casa (overround).
"""

from typing import Iterable, Tuple


def americana_a_implicita(cuota_americana: int) -> float:
    """Convierte una cuota en formato americano a probabilidad implícita (%)."""
    if cuota_americana == 0:
        return 0.0
    if cuota_americana > 0:
        return (100 / (cuota_americana + 100)) * 100
    return (abs(cuota_americana) / (abs(cuota_americana) + 100)) * 100


def calcular_overround(probabilidades: Iterable[float]) -> Tuple[float, float]:
    """
    Suma las probabilidades implícitas de un mercado y devuelve
    (total, margen_de_la_casa).
    """
    total = sum(probabilidades)
    margen = total - 100
    return total, margen


def detectar_value_bet(prob_implicita: float, prob_real_estimada: float) -> Tuple[bool, float]:
    """
    Compara la probabilidad real estimada contra la implícita del mercado.
    Devuelve (es_value_bet, ventaja_en_puntos_porcentuales).
    """
    ventaja = prob_real_estimada - prob_implicita
    return (ventaja > 0, ventaja)
