#!/usr/bin/env python3
"""
ID Checker - Comparador de IDs entre archivos CSV.

Aplicación con interfaz gráfica para comparar dos archivos CSV
y mostrar las diferencias entre sus IDs.

Uso:
    python id_checker.py
"""
import sys

MIN_PYTHON_VERSION = (3, 10)


def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    if sys.version_info < MIN_PYTHON_VERSION:
        print(
            f"Error: Se requiere Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]} o superior. "
            f"Versión actual: {sys.version_info.major}.{sys.version_info.minor}"
        )
        sys.exit(1)


def main():
    """Punto de entrada principal de la aplicación."""
    check_python_version()

    from src.ui.main_window import MainWindow

    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
