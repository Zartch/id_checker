"""
Módulo para comparación de IDs entre dos conjuntos.
"""
from dataclasses import dataclass

from .csv_parser import ParseResult


@dataclass
class ComparisonResult:
    """Resultado de la comparación entre dos archivos."""
    testing_filename: str
    target_filename: str
    testing_total: int
    target_total: int
    only_in_testing: list[str]
    only_in_target: list[str]
    testing_duplicates: dict[str, int]
    target_duplicates: dict[str, int]


def compare_ids(testing: ParseResult, target: ParseResult) -> ComparisonResult:
    """
    Compara los IDs de dos archivos y encuentra las diferencias.

    Args:
        testing: Resultado del parsing del archivo "Testing"
        target: Resultado del parsing del archivo "Target"

    Returns:
        ComparisonResult con las diferencias encontradas
    """
    testing_set = set(testing.ids)
    target_set = set(target.ids)

    only_in_testing = _get_original_format(
        testing_set - target_set,
        testing.ids
    )
    only_in_target = _get_original_format(
        target_set - testing_set,
        target.ids
    )

    return ComparisonResult(
        testing_filename=testing.filename,
        target_filename=target.filename,
        testing_total=testing.total_rows,
        target_total=target.total_rows,
        only_in_testing=sorted(only_in_testing),
        only_in_target=sorted(only_in_target),
        testing_duplicates=testing.duplicates,
        target_duplicates=target.duplicates
    )


def _get_original_format(ids_normalized: set[str], all_ids: list[str]) -> list[str]:
    """
    Recupera el formato original de los IDs (respetando mayúsculas/minúsculas).

    Como normalizamos a minúsculas, buscamos la primera aparición original.
    """
    original: dict[str, str] = {}
    for id_val in all_ids:
        normalized = id_val.lower() if isinstance(id_val, str) else id_val
        if normalized in ids_normalized and normalized not in original:
            original[normalized] = id_val

    return list(original.values())
