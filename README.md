# ID Checker

Aplicación de escritorio para comparar IDs entre dos archivos CSV y mostrar las diferencias.

## Requisitos

- Python 3.10 o superior
- Sistema operativo: Linux o Windows

No requiere dependencias externas (usa `tkinter`, incluido en Python).

## Uso

```bash
python id_checker.py
```

### Flujo de trabajo

1. Selecciona el archivo **Testing** (CSV con los IDs a verificar)
2. Selecciona el archivo **Target** (CSV de referencia)
3. Pulsa **Comparar archivos**
4. Revisa los resultados en pantalla

Los resultados se guardan automáticamente en la carpeta `resultados/`.

## Formato de CSV

Los archivos CSV deben cumplir:

| Característica | Valor |
|----------------|-------|
| Columnas | 1 (solo IDs) |
| Delimitador | Punto y coma (`;`) |
| Encoding | UTF-8 |
| Cabecera | Sí (primera fila) |

**Ejemplo válido:**
```csv
id
ABC123
DEF456
XYZ789
```

## Lógica de comparación

- **Case insensitive**: `ABC123` y `abc123` se consideran el mismo ID
- **Trim automático**: se ignoran espacios al inicio/final
- **Duplicados**: se detectan y muestran por separado

## Resultado

El resultado muestra:

- IDs en Testing que no están en Target
- IDs en Target que no están en Testing
- Duplicados encontrados en cada archivo

Los archivos de resultado se guardan en `resultados/` con formato:
```
id_checker_diff_YYYY-MM-DD_HHMMSS.txt
```

## Estructura del proyecto

```
id_checker/
├── id_checker.py          # Punto de entrada
├── src/
│   ├── csv_parser.py      # Lectura y validación de CSV
│   ├── comparator.py      # Lógica de comparación
│   ├── history_manager.py # Gestión de históricos
│   └── ui/
│       └── main_window.py # Interfaz gráfica
└── resultados/            # Históricos de comparaciones
```

## Licencia

MIT
