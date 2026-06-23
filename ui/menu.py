"""
Capa de presentación: todo lo relacionado con input() y print()
vive aquí, separado de la lógica de cálculo.
"""

from ui.colors import Colors
from core.market_analyzer import auditar_mercado, recomendar_apuesta, ResultadoMercado
from core.probability_model import EstadisticasEquipo, estimar_probabilidades_1x2


def mostrar_menu(version: str) -> None:
    print(f"\n{Colors.BOLD}{Colors.RED}" + "=" * 50)
    print(f" ⚡ P L A Y D O I T _ D I S T R O Y   V{version} ⚡")
    print("=" * 50 + f"{Colors.RESET}")
    print(f"[{Colors.GREEN}1{Colors.RESET}] PLAY")
    print(f"[{Colors.GREEN}0{Colors.RESET}] SALIR")


def pedir_opcion() -> str:
    return input(f"\n{Colors.CYAN}root@play:~# {Colors.RESET}")


def _mostrar_resultado_mercado(resultado: ResultadoMercado) -> None:
    print(f"\n{Colors.BOLD}[*] ANÁLISIS DEL MERCADO: {resultado.partido}{Colors.RESET}")
    print("-" * 45)
    for opcion in resultado.opciones:
        nombre_fmt = f"{opcion.nombre}:".ljust(13)
        print(f"Prob. {nombre_fmt} {opcion.probabilidad_implicita:>6.2f}% (Cuota: {opcion.cuota})")
    print("-" * 45)
    print(f"Suma Total de Probabilidades: {resultado.total_probabilidad:.2f}%")
    print(f"Margen de la Casa (Vig):      {Colors.YELLOW}{resultado.margen_casa:.2f}%{Colors.RESET}")
    print("-" * 45)


def _pedir_estadisticas(nombre_equipo: str) -> EstadisticasEquipo:
    print(f"\n{Colors.BOLD}Estadísticas recientes — {nombre_equipo}{Colors.RESET} (últimos partidos)")
    v = int(input("  Victorias: "))
    e = int(input("  Empates: "))
    d = int(input("  Derrotas: "))
    gf = int(input("  Goles a favor: "))
    gc = int(input("  Goles en contra: "))
    return EstadisticasEquipo(victorias=v, empates=e, derrotas=d, goles_favor=gf, goles_contra=gc)


def _mostrar_recomendacion(recomendacion) -> None:
    print(f"\n{Colors.BOLD}[*] RECOMENDACIÓN AUTOMÁTICA{Colors.RESET}")
    print("-" * 45)
    for d in recomendacion.todas:
        marca = f"{Colors.GREEN}+EV{Colors.RESET}" if d["es_valor"] else f"{Colors.RED}-EV{Colors.RESET}"
        print(
            f"{d['nombre']:<8} cuota {d['cuota']:>5} | mercado {d['prob_implicita']:>6.2f}% "
            f"| modelo {d['prob_estimada']:>6.2f}% | ventaja {d['ventaja']:>+6.2f}% [{marca}]"
        )
    print("-" * 45)
    if recomendacion.opcion:
        print(
            f"{Colors.GREEN}[+] RECOMENDACIÓN: Apostar a '{recomendacion.opcion}' "
            f"(ventaja estimada +{recomendacion.ventaja:.2f}%){Colors.RESET}"
        )
    else:
        print(f"{Colors.RED}[-] Sin recomendación: ninguna opción muestra valor positivo según el modelo.{Colors.RESET}")
    print(
        f"{Colors.YELLOW}[!] Nota: esto es una estimación de un modelo simple basado en forma reciente, "
        f"no una garantía de resultado.{Colors.RESET}"
    )


def flujo_auditoria_1x2() -> None:
    """Pide cuotas y estadísticas de ambos equipos, calcula el mercado y recomienda automáticamente."""
    print(f"\n{Colors.RED}--- APUESTA ---{Colors.RESET}")
    try:
        partido = input("Ingresa el partido (ej. Francia vs Irak): ")

        c_local = int(input(f"Cuota {Colors.BOLD}Local{Colors.RESET} (americana): "))
        c_empate = int(input(f"Cuota {Colors.BOLD}Empate{Colors.RESET} (americana): "))
        c_visita = int(input(f"Cuota {Colors.BOLD}Visita{Colors.RESET} (americana): "))

        resultado = auditar_mercado(
            partido, {"Local": c_local, "Empate": c_empate, "Visita": c_visita}
        )
        _mostrar_resultado_mercado(resultado)

        stats_local = _pedir_estadisticas("Local")
        stats_visita = _pedir_estadisticas("Visitante")

        probs_estimadas = estimar_probabilidades_1x2(stats_local, stats_visita)

        recomendacion = recomendar_apuesta(resultado, probs_estimadas)
        _mostrar_recomendacion(recomendacion)

    except ValueError:
        print(f"{Colors.RED}[!] Error de entrada. Se requieren valores numéricos.{Colors.RESET}")
