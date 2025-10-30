"""
Script ETL para normalizar archivos Excel del sistema de inventario AYNI.

Funcionalidades:
- Lee archivos Excel y detecta automáticamente la fila de encabezados
- Normaliza nombres de columnas
- Limpia datos inválidos (guiones, vacíos)
- Elimina filas con datos faltantes
- Elimina columnas sin datos válidos
- Exporta el resultado en formato Excel procesado

Uso:
    python ScriptETL.py archivo.xlsx
    python ScriptETL.py carpeta/ --output salida.xlsx
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List
import unicodedata
import pandas as pd

SheetConfig = Dict[str, object]


# Configuración de transformaciones por hoja


SHEET_RULES: Dict[str, SheetConfig] = {
	"stock": {
		"rename": {
			"Codigo Producto": "codigo",
			"Código Producto": "codigo",
			"Descripción": "nombre",
			"Descripcion": "nombre",
			"Und. de Medida": "unidadMedida",
			"UND. DE MEDIDA": "unidadMedida",
			"Unidad": "unidadMedida",
			"Costo U": "costoUnitario",
			"Costo U.": "costoUnitario",
			"Stock Actual": "stockActual",
			"Salidas": "salidas",
			"Ubicación": "ubicacion",
			"Proveedor": "proveedor",
			"Marca": "marca",
			"Categoría": "categoria",
		},
		"order": [
			"codigo",
			"nombre",
			"ubicacion",
			"salidas",
			"stockActual",
			"unidadMedida",
			"proveedor",
			"marca",
			"categoria",
			"costoUnitario",
		],
		"default_values": {
			"ubicacion": "ALMACEN PRINCIPAL",
			"salidas": 0,
			"stockActual": 0,
			"stockMinimo": 0,
			"unidadMedida": "UND",
			"providerId": 1,  # ID por defecto del proveedor
			"costoTotal": 0,
		},
		"required_columns": ["codigo", "nombre"],
	},
	"entradas": {
		"rename": {
			"Codigo Producto": "codigoProducto",
			"Código Producto": "codigoProducto",
			"Descripción": "descripcion",
			"Descripcion": "descripcion",
			"Costo U": "precioUnitario",
			"Costo U.": "precioUnitario",
			"Precio unitario": "precioUnitario",
			"Precio Unitario": "precioUnitario",
			"PRECIO UNITARIO": "precioUnitario",
			"Cantidad": "cantidad",
			"Área": "area",
			"Area": "area",
			"Responsable": "responsable",
			"Fecha": "fecha",
		},
		"order": [
			"fecha",
			"codigoProducto",
			"descripcion",
			"cantidad",
			"area",
			"precioUnitario",
			"responsable",
		],
		"default_values": {
			"precioUnitario": 0.0,
		},
		"required_columns": ["fecha", "codigoProducto", "descripcion", "cantidad"],
	},
	"salidas": {
		"rename": {
			"Fecha2": "fecha",
			"Fecha": "fecha",
			"Codigo de producto2": "codigoProducto",
			"Código de producto2": "codigoProducto",
			"Codigo de producto": "codigoProducto",
			"Código de producto": "codigoProducto",
			"Código producto": "codigoProducto",
			"CODIGO DE PRODUCTO": "codigoProducto",
			"Recisbio": "responsable",
			"Recibio": "responsable",
			"Recibió": "responsable",
			"Responsable": "responsable",
			"Descripción": "descripcion",
			"Descripcion": "descripcion",
			"Area": "area",
			"Área": "area",
			"AREA": "area",
			"Proyecto": "proyecto",
			"Cantidad": "cantidad",
			"Costo U": "precioUnitario",
			"Costo U.": "precioUnitario",
			"Precio unitario": "precioUnitario",
			"Precio Unitario": "precioUnitario",
			"Precio untitario2": "precioUnitario",
			"Precio untitario": "precioUnitario",
		},
		"drop_if_uppercase": ["descripcion"],
		"order": [
			"fecha",
			"codigoProducto",
			"descripcion",
			"area",
			"proyecto",
			"responsable",
			"cantidad",
			"precioUnitario",
		],
		"default_values": {
			"precioUnitario": 0.0,
		},
		"required_columns": ["fecha", "codigoProducto", "descripcion", "cantidad"],
	},
}


def normalize_name(name: str) -> str:
	"""Normaliza nombres eliminando acentos y convirtiendo a minúsculas."""

	normalized = unicodedata.normalize("NFKD", name)
	ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
	return ascii_only.strip().casefold()


def get_sheet_config(sheet_name: str) -> SheetConfig | None:
	"""Obtiene la configuración para una hoja específica."""

	return SHEET_RULES.get(normalize_name(sheet_name))


def sanitize_nombre_value(value: object) -> str:
	"""Limpia valores eliminando guiones y espacios vacíos."""

	if pd.isna(value):
		return ""

	if isinstance(value, str):
		stripped = value.strip()
		return "" if stripped in {"-", ""} else stripped

	# Convert non-string values to string while trimming whitespace.
	text = str(value).strip()
	return "" if text in {"-", ""} else text


def extract_numeric_value(value: object) -> int:
	"""Extrae solo el valor numérico de una celda, ignorando texto."""
	
	if pd.isna(value):
		return 0
	
	# Si ya es un número, retornarlo
	if isinstance(value, (int, float)):
		return int(value)
	
	# Si es string, extraer solo los dígitos
	if isinstance(value, str):
		# Remover todo excepto dígitos
		digits = ''.join(filter(str.isdigit, value))
		return int(digits) if digits else 0
	
	return 0


def is_valid_cell_value(value: object) -> bool:
	"""Verifica si un valor de celda es válido."""
	
	if pd.isna(value):
		return False
	
	if isinstance(value, str):
		stripped = value.strip()
		return stripped not in {"-", ""}
	
	# For numeric values, check if they're valid
	return True


def remove_invalid_rows(df: pd.DataFrame, required_columns: List[str]) -> pd.DataFrame:
	"""Elimina filas con datos faltantes en columnas requeridas."""
	
	if not required_columns:
		return df
	
	# Create a mask for valid rows
	valid_mask = pd.Series([True] * len(df), index=df.index)
	
	for column in required_columns:
		if column in df.columns:
			# Check each cell in the required column
			column_valid = df[column].apply(is_valid_cell_value)
			valid_mask = valid_mask & column_valid
	
	# Count removed rows for logging
	removed_count = (~valid_mask).sum()
	if removed_count > 0:
		print(f"  → Eliminadas {removed_count} filas con datos faltantes o inválidos")
	
	return df[valid_mask].reset_index(drop=True)


def remove_null_columns(df: pd.DataFrame) -> pd.DataFrame:
	"""Elimina columnas que están completamente vacías o con valores nulos/inválidos."""
	
	columns_to_keep = []
	columns_removed = []
	
	for column in df.columns:
		# Verificar si la columna tiene al menos un valor válido
		has_valid_data = df[column].apply(is_valid_cell_value).any()
		
		if has_valid_data:
			columns_to_keep.append(column)
		else:
			columns_removed.append(column)
	
	if columns_removed:
		print(f"  → Eliminadas {len(columns_removed)} columna(s) sin datos válidos: {', '.join(columns_removed)}")
	
	return df[columns_to_keep]


def collect_excel_files(target: Path) -> List[Path]:
	"""Recopila archivos Excel para procesar."""

	if target.is_file() and target.suffix.lower() in {".xlsx", ".xls"}:
		return [target]

	if target.is_dir():
		results = [
			path
			for path in target.rglob("*.xls*")
			if path.suffix.lower() in {".xlsx", ".xls"} and not path.name.startswith("~$")
		]
		return sorted(results)

	raise FileNotFoundError(f"Ruta no encontrada o no es un archivo de Excel: {target}")


def apply_sheet_rules(df: pd.DataFrame, config: SheetConfig | None) -> pd.DataFrame:
	"""Aplica reglas de transformación a la hoja."""

	if not config:
		return df

	updated = df.copy()

	drop_uppercase_targets = {
		normalize_name(label) for label in config.get("drop_if_uppercase", [])
	}
	if drop_uppercase_targets:
		columns_to_drop = [
			column
			for column in updated.columns
			if isinstance(column, str)
			and normalize_name(column) in drop_uppercase_targets
			and column.upper() == column
		]
		if columns_to_drop:
			updated = updated.drop(columns=columns_to_drop)

	rename_map = config.get("rename", {})
	if rename_map:
		# Normalizamos claves para coincidir aunque cambien las mayúsculas o acentos.
		normalized_columns = {
			normalize_name(column): column for column in updated.columns
		}
		for key, new_name in rename_map.items():
			normalized_key = normalize_name(key)
			if normalized_key in normalized_columns:
				original_column = normalized_columns[normalized_key]
				updated.rename(columns={original_column: new_name}, inplace=True)

	# Limpiar columnas de texto (nombre, descripcion)
	for text_column in ["nombre", "descripcion"]:
		if text_column in updated.columns:
			text_data = updated.loc[:, updated.columns == text_column]

			if isinstance(text_data, pd.DataFrame) and text_data.shape[1] > 1:
				merged = text_data.bfill(axis=1).iloc[:, 0].fillna("")
				updated = updated.loc[:, updated.columns != text_column]
				updated[text_column] = merged
			else:
				series = text_data.squeeze()
				updated = updated.drop(columns=[text_column])
				updated[text_column] = series.apply(sanitize_nombre_value)

	if "fecha" in updated.columns:
		fecha_series = pd.to_datetime(updated["fecha"], errors="coerce", dayfirst=False)
		formatted = fecha_series.dt.strftime("%d/%m/%Y")
		formatted = formatted.where(fecha_series.notna(), "")
		updated["fecha"] = formatted
	
	# Limpiar columna cantidad para que solo tenga valores numéricos
	if "cantidad" in updated.columns:
		updated["cantidad"] = updated["cantidad"].apply(extract_numeric_value)

	# Aplicar valores por defecto
	default_values = config.get("default_values", {})
	for column, default_value in default_values.items():
		if column not in updated.columns:
			updated[column] = default_value
		else:
			# Llenar valores nulos con el valor por defecto
			updated[column] = updated[column].fillna(default_value)
			# Si es string vacío, también aplicar default
			if isinstance(default_value, str):
				updated[column] = updated[column].replace("", default_value)

	for column in config.get("blank_columns", []):
		# Ensure the column exists and then clear its contents.
		if column not in updated.columns:
			updated[column] = ""
		else:
			updated[column] = ""

	desired_order: Iterable[str] = config.get("order", [])
	if desired_order:
		for column in desired_order:
			if column not in updated.columns:
				updated[column] = ""

		ordered = [col for col in desired_order if col in updated.columns]
		updated = updated[ordered]

	# Remove rows with invalid data in required columns
	required_columns = config.get("required_columns", [])
	if required_columns:
		updated = remove_invalid_rows(updated, required_columns)
	
	# Eliminar columnas que están completamente vacías o con valores nulos
	updated = remove_null_columns(updated)

	return updated


def find_header_row(excel_file, sheet_name: str, config: SheetConfig | None) -> int:
	"""Encuentra la fila donde están los encabezados reales."""
	
	if not config:
		return 0
	
	# Try to find the header row by looking for expected column names
	rename_map = config.get("rename", {})
	expected_columns = set(rename_map.keys()) | set(rename_map.values())
	
	# Read first 10 rows to find headers
	for header_row in range(10):
		try:
			df_test = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_row, nrows=0)
			columns_normalized = {normalize_name(str(col)) for col in df_test.columns}
			expected_normalized = {normalize_name(str(col)) for col in expected_columns}
			
			# If we find at least 2 matching column names, this is likely the header row
			matches = columns_normalized & expected_normalized
			if len(matches) >= 2:
				return header_row
		except Exception:
			continue
	
	return 0  # Default to first row if not found


def process_workbook(source: Path, destination: Path) -> Dict:
	"""Lee el archivo Excel, aplica transformaciones y retorna datos en formato dict."""

	excel_file = pd.ExcelFile(source)
	result = {}
	
	# Crear un writer de Excel (mode='w' para sobrescribir si existe)
	with pd.ExcelWriter(destination, engine='openpyxl', mode='w') as writer:
		for sheet in excel_file.sheet_names:
			config = get_sheet_config(sheet)
			
			# Find the correct header row
			header_row = find_header_row(excel_file, sheet, config)
			
			data = pd.read_excel(excel_file, sheet_name=sheet, header=header_row)
			original_rows = len(data)

			if config:
				print(f"\nProcesando hoja '{sheet}' ({original_rows} filas)...")
				data = apply_sheet_rules(data, config)
				final_rows = len(data)
				if final_rows < original_rows:
					print(f"  → Resultado: {final_rows} filas válidas")
			
			# Guardar la hoja procesada en el archivo Excel
			data.to_excel(writer, sheet_name=sheet, index=False)
			
			# También guardamos en el dict para retornar
			data_dict = data.where(pd.notnull(data), None).to_dict(orient='records')
			result[sheet] = data_dict
	
	return result


def build_destination_path(source: Path, output: str = None) -> Path:
	"""Construye la ruta de salida para el archivo Excel."""
	
	if output:
		return Path(output)
	
	# Agregar sufijo "_procesado" antes de la extensión
	return source.parent / f"{source.stem}_procesado{source.suffix}"


def parse_args() -> argparse.Namespace:
	"""Configura y parsea los argumentos de línea de comandos."""
	
	parser = argparse.ArgumentParser(
		description="Normaliza archivos Excel de inventario y exporta a Excel procesado"
	)
	parser.add_argument(
		"target",
		type=Path,
		help="Archivo Excel individual o carpeta con archivos Excel",
	)
	parser.add_argument(
		"--output",
		"-o",
		type=str,
		help="Ruta del archivo Excel de salida (por defecto: mismo nombre con sufijo _procesado)",
	)
	return parser.parse_args()


def main() -> None:
	"""Función principal del script."""
	
	args = parse_args()
	files = collect_excel_files(args.target)

	if not files:
		raise FileNotFoundError("No se encontraron archivos Excel para procesar")

	for file_path in files:
		output_path = build_destination_path(file_path, args.output)
		print(f"\nProcesando: {file_path.name}")
		process_workbook(file_path, output_path)
		print(f"\n✅ Archivo Excel procesado creado: {output_path}")
		print(f"Tamaño: {output_path.stat().st_size / 1024:.2f} KB")


if __name__ == "__main__":
	main()

