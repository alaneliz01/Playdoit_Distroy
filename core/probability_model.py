"""
Modelo heurístico para estimar la probabilidad "real" de cada resultado
a partir de estadísticas recientes de los equipos (no de las cuotas).

Esto NO es una predicción infalible: es un modelo simple basado en
fuerza ofensiva/defensiva y forma reciente. Sirve como punto de partida
para comparar contra el mercado, no como garantía de resultado.
"""

from dataclasses import dataclass


@dataclass
class EstadisticasEquipo:
    victorias: int
    empates: int
    derrotas: int
    goles_favor: int
    goles_contra: int

    @property
    def partidos(self) -> int:
        return max(self.victorias + self.empates + self.derrotas, 1)

    @property
    def fuerza_ofensiva(self) -> float:
        return self.goles_favor / self.partidos

    @property
    def fuerza_defensiva(self) -> float:
        # Menor = mejor defensa. Evitamos división por cero.
        return self.goles_contra / self.partidos

    @property
    def puntos_por_partido(self) -> float:
        return (self.victorias * 3 + self.empates) / self.partidos


def estimar_probabilidades_1x2(local: EstadisticasEquipo, visitante: EstadisticasEquipo,
                                ventaja_local: float = 0.10) -> dict:
    """
    Devuelve {"Local": %, "Empate": %, "Visita": %} estimados a partir
    de la forma reciente de ambos equipos.

    ventaja_local: bonus por jugar en casa (10% por defecto).
    """
    # "Poder" relativo = ataque propio vs defensa rival + puntos por partido
    poder_local = (local.fuerza_ofensiva - visitante.fuerza_defensiva) + local.puntos_por_partido
    poder_visita = (visitante.fuerza_ofensiva - local.fuerza_defensiva) + visitante.puntos_por_partido

    # Evitar negativos extremos
    poder_local = max(poder_local, 0.1)
    poder_visita = max(poder_visita, 0.1)

    poder_local *= (1 + ventaja_local)

    total_poder = poder_local + poder_visita
    prob_local_base = poder_local / total_poder
    prob_visita_base = poder_visita / total_poder

    # El empate es más probable cuanto más parejos están los equipos
    paridad = 1 - abs(prob_local_base - prob_visita_base)
    prob_empate = 20 + (paridad * 15)  # rango aprox. 20%-35%

    restante = 100 - prob_empate
    prob_local = restante * prob_local_base
    prob_visita = restante * prob_visita_base

    return {
        "Local": round(prob_local, 2),
        "Empate": round(prob_empate, 2),
        "Visita": round(prob_visita, 2),
    }
