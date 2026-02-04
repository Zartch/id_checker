"""
Módulo para lectura y validación de archivos CSV.
"""
import csv
from dataclasses import dataclass
from pathlib import Path


class CSVValidationError(Exception):
    """Error de validación del archivo CSV."""
    pass


@dataclass
class ParseResult:
    """Resultado del parsing de un CSV."""
    ids: list[str]
    duplicates: dict[str, int]  # ID -> número de apariciones
    filename: str
    total_rows: int


def parse_csv(filepath: str | Path) -> ParseResult:
    """
    Lee un archivo CSV y extrae los IDs.

    Args:
        filepath: Ruta al archivo CSV

    Returns:
        ParseResult con los IDs encontrados y duplicados

    Raises:
        CSVValidationError: Si el archivo no cumple el formato esperado
        FileNotFoundError: Si el archivo no existe
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

    if not filepath.suffix.lower() == '.csv':
        raise CSVValidationError("El archivo debe tener extensión .csv")

    ids_raw: list[str] = []

    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        header = next(reader, None)
        if header is None:
            raise CSVValidationError("El archivo está vacío")

        if len(header) > 1:
            raise CSVValidationError(
                f"El archivo debe tener solo 1 columna, pero tiene {len(header)}"
            )

        for line_number, row in enumerate(reader, start=2):
            if len(row) > 1:
                raise CSVValidationError(
                    f"Línea {line_number}: se esperaba 1 columna, se encontraron {len(row)}"
                )

            if row:
                id_value = row[0].strip()
                if id_value:
                    ids_raw.append(id_value)

    ids_normalized = [id_val.lower() for id_val in ids_raw]
    duplicates = _find_duplicates(ids_normalized, ids_raw)
    unique_ids = list(dict.fromkeys(ids_normalized))

    return ParseResult(
        ids=unique_ids,
        duplicates=duplicates,
        filename=filepath.name,
        total_rows=len(ids_raw)
    )


def _find_duplicates(ids_normalized: list[str], ids_original: list[str]) -> dict[str, int]:
    """
    Encuentra IDs duplicados y cuenta sus apariciones.

    Devuelve el formato original (primera aparición) para mostrar al usuario.
    """
    count: dict[str, int] = {}
    original_format: dict[str, str] = {}

    for normalized, original in zip(ids_normalized, ids_original):
        count[normalized] = count.get(normalized, 0) + 1
        if normalized not in original_format:
            original_format[normalized] = original

    return {
        original_format[normalized]: appearances
        for normalized, appearances in count.items()
        if appearances > 1
    }
