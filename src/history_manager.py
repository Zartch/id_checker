"""
Módulo para gestión de archivos históricos de resultados.
"""
from datetime import datetime
from pathlib import Path

from .comparator import ComparisonResult


RESULTS_FOLDER_NAME = "resultados"
FILE_PREFIX = "id_checker_diff_"


def get_results_folder() -> Path:
    """Obtiene la carpeta de resultados junto al ejecutable."""
    script_dir = Path(__file__).parent.parent
    results_folder = script_dir / RESULTS_FOLDER_NAME
    results_folder.mkdir(exist_ok=True)
    return results_folder


def get_history_files() -> list[Path]:
    """
    Obtiene la lista de archivos históricos ordenados por fecha (más reciente primero).
    """
    results_folder = get_results_folder()
    files = list(results_folder.glob(f"{FILE_PREFIX}*.txt"))
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)


def save_result(result: ComparisonResult) -> Path:
    """
    Guarda el resultado de una comparación en un archivo de texto.

    Returns:
        Path del archivo guardado
    """
    results_folder = get_results_folder()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"{FILE_PREFIX}{timestamp}.txt"
    filepath = results_folder / filename

    content = _format_result(result)
    filepath.write_text(content, encoding='utf-8')

    return filepath


def read_history_file(filepath: Path) -> str:
    """Lee el contenido de un archivo histórico."""
    return filepath.read_text(encoding='utf-8')


def _format_result(result: ComparisonResult) -> str:
    """Formatea el resultado de comparación para guardarlo como texto."""
    separator = "=" * 80
    subseparator = "-" * 80
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        separator,
        "ID CHECKER - Resultado de comparación",
        separator,
        f"Fecha: {timestamp}",
        f"Archivo Testing: {result.testing_filename} ({result.testing_total} IDs)",
        f"Archivo Target: {result.target_filename} ({result.target_total} IDs)",
        separator,
        "",
        f">> IDs en TESTING que NO están en TARGET ({len(result.only_in_testing)}):",
        subseparator,
    ]

    if result.only_in_testing:
        lines.extend(result.only_in_testing)
    else:
        lines.append("(ninguno)")

    lines.extend([
        "",
        f">> IDs en TARGET que NO están en TESTING ({len(result.only_in_target)}):",
        subseparator,
    ])

    if result.only_in_target:
        lines.extend(result.only_in_target)
    else:
        lines.append("(ninguno)")

    lines.extend([
        "",
        f">> Duplicados encontrados en TESTING ({len(result.testing_duplicates)}):",
        subseparator,
    ])

    if result.testing_duplicates:
        for id_val, count in sorted(result.testing_duplicates.items()):
            lines.append(f"{id_val} (aparece {count} veces)")
    else:
        lines.append("(ninguno)")

    lines.extend([
        "",
        f">> Duplicados encontrados en TARGET ({len(result.target_duplicates)}):",
        subseparator,
    ])

    if result.target_duplicates:
        for id_val, count in sorted(result.target_duplicates.items()):
            lines.append(f"{id_val} (aparece {count} veces)")
    else:
        lines.append("(ninguno)")

    lines.extend(["", separator])

    return "\n".join(lines)
