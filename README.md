# Script ETL - AYNI Almacén

Script para normalizar y limpiar archivos Excel del sistema de inventario AYNI, exportando los resultados en formato JSON.

## Funcionalidades

- Detecta automáticamente la fila de encabezados en cada hoja
- Normaliza nombres de columnas
- Limpia datos inválidos (guiones, valores vacíos)
- Elimina filas con datos faltantes en columnas críticas
- Exporta el resultado en formato JSON

## Hojas Procesadas

- **Stock**: Inventario actual de productos
- **Entradas**: Registro de entradas al almacén
- **Salidas**: Registro de salidas del almacén

## Uso

### Básico
```bash
python ScriptETL.py archivo.xlsx
```

Genera un archivo JSON con el mismo nombre que el Excel.

### Con nombre de salida personalizado
```bash
python ScriptETL.py archivo.xlsx --output resultado.json
python ScriptETL.py archivo.xlsx -o resultado.json
```

### Procesar múltiples archivos
```bash
python ScriptETL.py carpeta/
```

## Ejemplo de Salida

El JSON generado tiene la siguiente estructura:

```json
{
  "Stock": [
    {
      "Código": "AF2025",
      "Nombre": "AFLOJA TODO",
      "Ubicación": "",
      "Salidas": 14,
      "Stock Actual": 4,
      "Unidad": "und",
      "Proveedor": null,
      "Marca": "",
      "Categoría": "",
      "Costo Unitario": 10.0
    }
  ],
  "Entradas": [...],
  "Salidas": [...]
}
```

## Validaciones Aplicadas

### Stock
- Columnas requeridas: Código, Nombre

### Entradas
- Columnas requeridas: Fecha, Código, Nombre, Cantidad

### Salidas
- Columnas requeridas: Fecha, Código, Nombre, Cantidad

Las filas que no cumplan con tener valores válidos en todas las columnas requeridas serán eliminadas automáticamente.

## Requisitos

```bash
pip install pandas openpyxl
```
