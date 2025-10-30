# Script ETL - AYNI Almacén# Script ETL - AYNI Almacén# Script ETL - AYNI Almacén



Scripts para normalizar, limpiar y convertir archivos Excel del sistema de inventario AYNI a formato Excel procesado y SQL para PostgreSQL.



## 📦 ComponentesScripts para normalizar, limpiar y convertir archivos Excel del sistema de inventario AYNI a formato Excel procesado y SQL para PostgreSQL.Script para normalizar y limpiar archivos Excel del sistema de inventario AYNI, exportando los resultados en formato JSON.



### 1. ScriptETL.py

Normaliza y limpia archivos Excel del inventario, generando un archivo Excel procesado con datos validados listos para importar a la base de datos.

## 📦 Componentes## Funcionalidades

**Características:**

- Detecta automáticamente la fila de encabezados en cada hoja

- Normaliza nombres de columnas según el schema de Prisma (camelCase)

- Limpia datos inválidos (guiones, valores vacíos, textos en campos numéricos)### 1. ScriptETL.py- Detecta automáticamente la fila de encabezados en cada hoja

- Elimina filas con datos faltantes en columnas críticas

- Elimina columnas completamente vacías sin datos válidosNormaliza y limpia archivos Excel del inventario, generando un Excel procesado con datos validados.- Normaliza nombres de columnas

- Extrae valores numéricos de campos de cantidad (ej: "1 unidad" → 1)

- Formatea fechas al estándar DD/MM/YYYY- Limpia datos inválidos (guiones, valores vacíos)

- Aplica valores por defecto según el schema de Prisma

- Exporta resultados en formato Excel (`archivo_procesado.xlsx`)**Características:**- Elimina filas con datos faltantes en columnas críticas



### 2. GenerateSQL.py- Detecta automáticamente la fila de encabezados en cada hoja- Exporta el resultado en formato JSON

Convierte el Excel procesado a sentencias SQL INSERT compatibles con PostgreSQL y el schema de Prisma.

- Normaliza nombres de columnas según el schema de Prisma

**Características:**

- Genera SQL con manejo correcto de claves foráneas- Limpia datos inválidos (guiones, valores vacíos, textos en campos numéricos)## Hojas Procesadas

- Escapado automático de comillas simples

- Manejo de valores NULL- Elimina filas con datos faltantes en columnas críticas

- Timestamps automáticos con NOW()

- Compatible con el schema de Prisma del proyecto- Elimina columnas completamente vacías sin datos válidos- **Stock**: Inventario actual de productos



## 📊 Hojas Procesadas- Extrae valores numéricos de campos de cantidad (ej: "1 unidad" → 1)- **Entradas**: Registro de entradas al almacén



- **Stock → products**: Inventario actual de productos (93 productos)- Formatea fechas al estándar DD/MM/YYYY- **Salidas**: Registro de salidas del almacén

- **Entradas → movement_entries**: Registro de entradas al almacén (146 entradas)

- **Salidas → movement_exits**: Registro de salidas del almacén (2,317 salidas)- Exporta resultados en formato Excel



## 🚀 Uso## Uso



### 1. Procesar Excel### 2. GenerateSQL.py

```bash

python ScriptETL.py "archivo.xlsx"Convierte el Excel procesado a sentencias SQL INSERT compatibles con PostgreSQL y el schema de Prisma.### Básico

```

```bash

Genera un archivo Excel procesado: `archivo_procesado.xlsx`

**Características:**python ScriptETL.py archivo.xlsx

**Ejemplo:**

```bash- Genera SQL con manejo correcto de claves foráneas```

python ScriptETL.py "CONTROL INVENTARIO EPP ACTUAL FIRME 2025.xlsx"

```- Escapado automático de comillas simples



**Salida esperada:**- Manejo de valores NULLGenera un archivo JSON con el mismo nombre que el Excel.

```

Procesando hoja 'Stock' (933 filas)...- Timestamps automáticos con NOW()

  → Eliminadas 840 filas con datos faltantes o inválidos

  → Eliminadas 3 columna(s) sin datos válidos: proveedor, marca, categoria- Compatible con el schema de Prisma### Con nombre de salida personalizado

  → Resultado: 93 filas válidas

```bash

✅ Archivo Excel procesado creado: ...procesado.xlsx

Tamaño: 92.13 KB## 📊 Hojas Procesadaspython ScriptETL.py archivo.xlsx --output resultado.json

```

python ScriptETL.py archivo.xlsx -o resultado.json

### 2. Generar SQL

```bash- **Stock → products**: Inventario actual de productos (93 productos)```

python GenerateSQL.py "archivo_procesado.xlsx"

```- **Entradas → movement_entries**: Registro de entradas al almacén (145 entradas)



Genera un archivo SQL: `archivo_procesado.sql`- **Salidas → movement_exits**: Registro de salidas del almacén (2,317 salidas)### Procesar múltiples archivos



**Ejemplo:**```bash

```bash

python GenerateSQL.py "CONTROL INVENTARIO EPP ACTUAL FIRME 2025_procesado.xlsx"## 🚀 Usopython ScriptETL.py carpeta/

```

```

**Salida esperada:**

```### 1. Procesar Excel

Datos cargados:

  - Productos (Stock): 93 registros```bash## Ejemplo de Salida

  - Entradas: 146 registros

  - Salidas: 2317 registrospython ScriptETL.py "archivo.xlsx"



✅ Archivo SQL generado: ...procesado.sql```El JSON generado tiene la siguiente estructura:

Tamaño: 658 KB

```



## 📋 Mapeo de ColumnasGenera un archivo Excel procesado: `archivo_procesado.xlsx````json



### Stock → products{

| Columna Original | Columna BD | Tipo | Default |

|-----------------|------------|------|---------|**Ejemplo:**  "Stock": [

| Código Producto | `codigo` | String (único) | - |

| Descripción/Nombre | `nombre` | String | - |```bash    {

| Costo U/Costo U. | `costoUnitario` | Float | - |

| Ubicación | `ubicacion` | String | "ALMACEN PRINCIPAL" |python ScriptETL.py "CONTROL INVENTARIO EPP ACTUAL FIRME 2025.xlsx"      "Código": "AF2025",

| Salidas | `salidas` | Int | 0 |

| Stock Actual | `stockActual` | Int | 0 |```      "Nombre": "AFLOJA TODO",

| - | `stockMinimo` | Int | 0 |

| Und. de Medida/Unidad | `unidadMedida` | String | "UND" |      "Ubicación": "",

| - | `providerId` | Int | 1 |

| - | `costoTotal` | Float | 0 |### 2. Generar SQL      "Salidas": 14,



### Entradas → movement_entries```bash      "Stock Actual": 4,

| Columna Original | Columna BD | Tipo | Default |

|-----------------|------------|------|---------|python GenerateSQL.py "archivo_procesado.xlsx"      "Unidad": "und",

| Fecha | `fecha` | String (DD/MM/YYYY) | - |

| Código Producto | `codigoProducto` | String (FK) | - |```      "Proveedor": null,

| Descripción | `descripcion` | String | - |

| Cantidad | `cantidad` | Int | - |      "Marca": "",

| Precio unitario/Costo U | `precioUnitario` | Float | 0.0 |

| Área | `area` | String | NULL |Genera un archivo SQL: `archivo_procesado.sql`      "Categoría": "",

| Responsable | `responsable` | String | NULL |

      "Costo Unitario": 10.0

### Salidas → movement_exits

| Columna Original | Columna BD | Tipo | Default |**Ejemplo:**    }

|-----------------|------------|------|---------|

| Fecha2 | `fecha` | String (DD/MM/YYYY) | - |```bash  ],

| Codigo de producto2 | `codigoProducto` | String (FK) | - |

| Descripción | `descripcion` | String | - |python GenerateSQL.py "CONTROL INVENTARIO EPP ACTUAL FIRME 2025_procesado.xlsx"  "Entradas": [...],

| Cantidad | `cantidad` | Int | - |

| Precio untitario2 | `precioUnitario` | Float | 0.0 |```  "Salidas": [...]

| Recisbio/Responsable | `responsable` | String | NULL |

| Area/AREA | `area` | String | NULL |}

| Proyecto | `proyecto` | String | NULL |

## 📋 Mapeo de Columnas```

## ⚙️ Validaciones y Limpieza Aplicadas



### Validaciones por Tabla

- **Stock**: Requiere `codigo` y `nombre`### Stock → products## Validaciones Aplicadas

- **Entradas**: Requiere `fecha`, `codigoProducto`, `descripcion` y `cantidad`

- **Salidas**: Requiere `fecha`, `codigoProducto`, `descripcion` y `cantidad`| Columna Original | Columna BD | Tipo | Default |



### Limpieza Automática|-----------------|------------|------|---------|### Stock

- ✅ Extracción de valores numéricos en campo `cantidad` (elimina texto, deja solo números)

- ✅ Eliminación de columnas completamente vacías o con solo valores nulos| Código Producto | `codigo` | String (único) | - |- Columnas requeridas: Código, Nombre

- ✅ Eliminación de filas con datos faltantes en columnas requeridas

- ✅ Formato de fechas estandarizado a DD/MM/YYYY| Descripción/Nombre | `nombre` | String | - |

- ✅ Limpieza de valores inválidos (guiones "-", espacios vacíos)

- ✅ Escapado de caracteres especiales para SQL (comillas simples)| Costo U/Costo U. | `costoUnitario` | Float | - |### Entradas



### Columnas Eliminadas Automáticamente (del Excel de ejemplo)| Ubicación | `ubicacion` | String | "ALMACEN PRINCIPAL" |- Columnas requeridas: Fecha, Código, Nombre, Cantidad

**Stock:** proveedor, marca, categoria (sin datos válidos)  

**Entradas:** area, responsable (sin datos válidos)  | Salidas | `salidas` | Int | 0 |

**Salidas:** proyecto (sin datos válidos)

| Stock Actual | `stockActual` | Int | 0 |### Salidas

## 📝 Requisitos Previos

| - | `stockMinimo` | Int | 0 |- Columnas requeridas: Fecha, Código, Nombre, Cantidad

### Para ejecutar los scripts:

```bash| Und. de Medida/Unidad | `unidadMedida` | String | "UND" |

pip install pandas openpyxl

```| - | `providerId` | Int | 1 |Las filas que no cumplan con tener valores válidos en todas las columnas requeridas serán eliminadas automáticamente.



### Para ejecutar el SQL generado:| - | `costoTotal` | Float | 0 |

Debe existir al menos un proveedor con ID=1 en la base de datos:

```sql## Requisitos

INSERT INTO providers (name, email, address, phones, "createdAt", "updatedAt")

VALUES ('Proveedor General', 'general@proveedor.com', 'Sin dirección', ARRAY[]::text[], NOW(), NOW());### Entradas → movement_entries

```

| Columna Original | Columna BD | Tipo | Default |```bash

## 🎯 Flujo de Trabajo Completo

|-----------------|------------|------|---------|pip install pandas openpyxl

```bash

# 1. Procesar el Excel original| Fecha | `fecha` | String (DD/MM/YYYY) | - |```

python ScriptETL.py "CONTROL INVENTARIO EPP ACTUAL FIRME 2025.xlsx"

# Resultado: CONTROL INVENTARIO EPP ACTUAL FIRME 2025_procesado.xlsx| Código Producto | `codigoProducto` | String (FK) | - |

| Descripción | `descripcion` | String | - |

# 2. Generar SQL desde el Excel procesado| Cantidad | `cantidad` | Int | - |

python GenerateSQL.py "CONTROL INVENTARIO EPP ACTUAL FIRME 2025_procesado.xlsx"| Precio unitario/Costo U | `precioUnitario` | Float | 0.0 |

# Resultado: CONTROL INVENTARIO EPP ACTUAL FIRME 2025_procesado.sql| Área | `area` | String | NULL |

| Responsable | `responsable` | String | NULL |

# 3. Ejecutar en PostgreSQL

# Opción A: Desde línea de comandos### Salidas → movement_exits

psql -U usuario -d basededatos -f "CONTROL INVENTARIO EPP ACTUAL FIRME 2025_procesado.sql"| Columna Original | Columna BD | Tipo | Default |

|-----------------|------------|------|---------|

# Opción B: Copiar y pegar en pgAdmin o DBeaver| Fecha2 | `fecha` | String (DD/MM/YYYY) | - |

# Abre el archivo .sql y copia su contenido en tu cliente SQL| Codigo de producto2 | `codigoProducto` | String (FK) | - |

```| Descripción | `descripcion` | String | - |

| Cantidad | `cantidad` | Int | - |

## 📤 Ejemplo de SQL Generado| Precio untitario2 | `precioUnitario` | Float | 0.0 |

| Recisbio/Responsable | `responsable` | String | NULL |

El archivo SQL incluye:| Area/AREA | `area` | String | NULL |

- Instrucciones para crear el proveedor por defecto| Proyecto | `proyecto` | String | NULL |

- INSERT de 93 productos en tabla `products`

- INSERT de 146 entradas en tabla `movement_entries`## ⚙️ Validaciones y Limpieza Aplicadas

- INSERT de 2,317 salidas en tabla `movement_exits`

### Validaciones por Tabla

**Fragmento del SQL generado:**- **Stock**: Requiere `codigo` y `nombre`

```sql- **Entradas**: Requiere `fecha`, `codigoProducto`, `descripcion` y `cantidad`

-- ============================================- **Salidas**: Requiere `fecha`, `codigoProducto`, `descripcion` y `cantidad`

-- INSERCIÓN DE PRODUCTOS (products)

-- ============================================### Limpieza Automática

- ✅ Extracción de valores numéricos en campo `cantidad` (elimina texto, deja solo números)

INSERT INTO products (codigo, nombre, "costoUnitario", ubicacion, salidas, "stockActual", "stockMinimo", "unidadMedida", "providerId", "costoTotal", "createdAt", "updatedAt")- ✅ Eliminación de columnas completamente vacías o con solo valores nulos

VALUES ('CAN64', 'Canguro', 15.0, 'CHALECO', 10, 6, 0, 'UND', 1, 0, NOW(), NOW());- ✅ Eliminación de filas con datos faltantes en columnas requeridas

- ✅ Formato de fechas estandarizado a DD/MM/YYYY

-- ============================================- ✅ Limpieza de valores inválidos (guiones "-", espacios vacíos)

-- INSERCIÓN DE ENTRADAS (movement_entries)- ✅ Escapado de caracteres especiales para SQL (comillas simples)

-- ============================================

### Columnas Eliminadas Automáticamente

INSERT INTO movement_entries (fecha, "codigoProducto", descripcion, "precioUnitario", cantidad, "createdAt", "updatedAt")**Stock:** proveedor, marca, categoria (sin datos válidos)  

VALUES ('07/05/2024', 'CAN64', 'Canguro', 15.0, 5, NOW(), NOW());**Entradas:** area, responsable (sin datos válidos)  

**Salidas:** proyecto (sin datos válidos)

-- ============================================

-- INSERCIÓN DE SALIDAS (movement_exits)## 📝 Requisitos Previos

-- ============================================

### Para ejecutar los scripts:

INSERT INTO movement_exits (fecha, "codigoProducto", descripcion, "precioUnitario", cantidad, responsable, area, proyecto, "createdAt", "updatedAt")```bash

VALUES ('07/05/2024', 'CAN64', 'Canguro', 15.0, 1, 'GUSTAVO', 'MECANICA', NULL, NOW(), NOW());pip install pandas openpyxl

``````



## 🔗 Integración con Prisma### Para ejecutar el SQL generado:

Debe existir al menos un proveedor con ID=1 en la base de datos:

Los datos generados son 100% compatibles con el schema de Prisma del proyecto:```sql

INSERT INTO providers (name, email, address, phones, "createdAt", "updatedAt")

**Relaciones de clave foránea:**VALUES ('Proveedor General', 'general@proveedor.com', 'Sin dirección', ARRAY[]::text[], NOW(), NOW());

- `products.codigo` ← `movement_entries.codigoProducto````

- `products.codigo` ← `movement_exits.codigoProducto`

- `products.providerId` → `providers.id`## 🎯 Ejemplo de Uso Completo



**Campos automáticos:**```bash

- `createdAt`: Se establece con NOW()# 1. Procesar el Excel

- `updatedAt`: Se establece con NOW()python ScriptETL.py "CONTROL INVENTARIO EPP ACTUAL FIRME 2025.xlsx"



## 📊 Resultados Estadísticos# Salida:

# Procesando hoja 'Stock' (933 filas)...

Basado en el Excel de ejemplo procesado:#   → Eliminadas 840 filas con datos faltantes o inválidos

#   → Eliminadas 3 columna(s) sin datos válidos: proveedor, marca, categoria

| Tabla | Filas Originales | Filas Procesadas | Columnas Eliminadas |#   → Resultado: 93 filas válidas

|-------|-----------------|------------------|---------------------|# ✅ Archivo Excel procesado creado: ...procesado.xlsx

| Stock | 933 | 93 | 3 (proveedor, marca, categoria) |

| Entradas | 458 | 146 | 2 (area, responsable) |# 2. Generar SQL

| Salidas | 2,460 | 2,317 | 1 (proyecto) |python GenerateSQL.py "CONTROL INVENTARIO EPP ACTUAL FIRME 2025_procesado.xlsx"



**Tamaño de archivos:**# Salida:

- Excel procesado: ~92 KB# Datos cargados:

- SQL generado: ~658 KB#   - Productos (Stock): 93 registros

#   - Entradas: 146 registros

## 🛠️ Troubleshooting#   - Salidas: 2317 registros

# ✅ Archivo SQL generado: ...procesado.sql (658 KB)

### Error: "Permission denied" al generar Excel

**Causa:** El archivo de salida está abierto en Excel  # 3. Ejecutar en PostgreSQL

**Solución:** Cierra el archivo Excel y vuelve a ejecutar el scriptpsql -U usuario -d basededatos -f "CONTROL INVENTARIO EPP ACTUAL FIRME 2025_procesado.sql"

```

### Error: "INSERT 0 1" en PostgreSQL

**Significado:** ✅ Todo está bien. Cada INSERT se ejecutó correctamente## 📤 Salida SQL Generada



### Error: "foreign key constraint" en SQLEl SQL generado incluye:

**Causa:** No existe el proveedor con ID=1  - Creación del proveedor por defecto (instrucciones)

**Solución:** Ejecuta primero el INSERT del proveedor mencionado en "Requisitos Previos"- INSERT de 93 productos en `products`

- INSERT de 146 entradas en `movement_entries`

## 📄 Licencia- INSERT de 2,317 salidas en `movement_exits`



Desarrollado para AYNI SAC - Sistema de Inventario**Ejemplo de SQL generado:**

```sql
-- Productos
INSERT INTO products (codigo, nombre, "costoUnitario", ubicacion, salidas, "stockActual", "stockMinimo", "unidadMedida", "providerId", "costoTotal", "createdAt", "updatedAt")
VALUES ('CAN64', 'Canguro', 15.0, 'CHALECO', 10, 6, 0, 'UND', 1, 0, NOW(), NOW());

-- Entradas
INSERT INTO movement_entries (fecha, "codigoProducto", descripcion, "precioUnitario", cantidad, "createdAt", "updatedAt")
VALUES ('07/05/2024', 'CAN64', 'Canguro', 15.0, 5, NOW(), NOW());

-- Salidas
INSERT INTO movement_exits (fecha, "codigoProducto", descripcion, "precioUnitario", cantidad, responsable, area, proyecto, "createdAt", "updatedAt")
VALUES ('07/05/2024', 'CAN64', 'Canguro', 15.0, 1, 'GUSTAVO', 'MECANICA', NULL, NOW(), NOW());
```

## 🔗 Integración con Prisma

Los datos generados son compatibles con el schema de Prisma del proyecto:
- Relaciones de clave foránea: `products.codigo` ← `movement_entries.codigoProducto` / `movement_exits.codigoProducto`
- Relación de proveedor: `products.providerId` → `providers.id`
- Timestamps automáticos: `createdAt`, `updatedAt`

## 📄 Licencia

Desarrollado para AYNI SAC - Sistema de Inventario
