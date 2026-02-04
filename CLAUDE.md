# CLAUDE.md - Guía para AI Assistant en id_checker

## Descripción del Proyecto

**id_checker** es una aplicación de escritorio con GUI para comparar IDs entre dos archivos CSV y mostrar las diferencias.

**Repositorio**: Zartch/id_checker
**Lenguaje**: Python 3.10+
**Framework GUI**: tkinter (incluido en Python)

## Cómo Ejecutar

```bash
python id_checker.py
```

No requiere instalación de dependencias externas.

## Estructura del Proyecto

```
id_checker/
├── CLAUDE.md              # Esta guía
├── requirements.txt       # Dependencias (solo para empaquetado opcional)
├── id_checker.py          # Punto de entrada principal
├── src/
│   ├── __init__.py
│   ├── csv_parser.py      # Lectura y validación de CSV
│   ├── comparator.py      # Lógica de comparación de IDs
│   ├── history_manager.py # Gestión de archivos históricos
│   └── ui/
│       ├── __init__.py
│       └── main_window.py # Ventana principal
└── resultados/            # Archivos históricos de comparaciones
```

## Formato de CSV Esperado

- **Delimitador**: punto y coma (`;`)
- **Encoding**: UTF-8
- **Columnas**: exactamente 1 columna
- **Cabecera**: sí, primera fila es cabecera

Ejemplo válido:
```csv
id
ABC123
DEF456
XYZ789
```

## Lógica de Comparación

- **Case insensitive**: `ABC123` y `abc123` son el mismo ID
- **Trim automático**: se eliminan espacios al inicio/final
- **Duplicados**: se detectan y muestran por separado

## Convenciones de Código

### Estilo

- Python 3.10+ con type hints
- Nombres de funciones y variables en snake_case
- Clases en PascalCase
- Docstrings en español para módulos, inglés técnico aceptable en código

### Imports

1. Biblioteca estándar
2. Terceros (si los hubiera)
3. Módulos locales

### Principios

- SOLID
- Funciones pequeñas con nombres autoexplicativos
- Comentarios solo cuando el código no se explica solo
- Sin over-engineering

## Git Workflow

### Commits

Formato conventional commits:
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bugs
- `docs:` - Documentación
- `refactor:` - Refactorización
- `chore:` - Mantenimiento

### Branches

- Features: `feature/<descripcion>`
- Fixes: `fix/<descripcion>`
- Claude: `claude/<session-id>`

## Archivos Históricos

- **Ubicación**: carpeta `resultados/` junto al ejecutable
- **Formato nombre**: `id_checker_diff_YYYY-MM-DD_HHMMSS.txt`
- **Contenido**: texto plano legible

## Notas para el AI Assistant

1. Mantener la simplicidad - evitar abstracciones innecesarias
2. El código debe autoexplicarse con nombres claros
3. Preferir editar archivos existentes antes que crear nuevos
4. Probar cambios antes de commitear
