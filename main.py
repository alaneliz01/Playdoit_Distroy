"""
Punto de entrada de la aplicación. Solo se encarga de orquestar
el menú principal; toda la lógica vive en core/ y ui/.
"""

import sys

from ui.colors import Colors
from ui.menu import mostrar_menu, pedir_opcion, flujo_auditoria_1x2

VERSION = "1.0"


def ejecutar() -> None:
    while True:
        mostrar_menu(VERSION)
        opcion = pedir_opcion()

        if opcion == "0":
            print("\n[Cerrando sesión de auditoría...]")
            break
        elif opcion == "1":
            flujo_auditoria_1x2()
        else:
            print(f"{Colors.RED}[!] Comando no reconocido.{Colors.RESET}")


if __name__ == "__main__":
    try:
        ejecutar()
    except KeyboardInterrupt:
        print("\n\n[!] Ejecución interrumpida por el usuario. Saliendo...")
        sys.exit(0)
