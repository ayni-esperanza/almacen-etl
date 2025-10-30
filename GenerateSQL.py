"""
Script para generar sentencias SQL INSERT desde el Excel procesado.
Genera SQL compatible con PostgreSQL y el schema de Prisma.
"""

import pandas as pd
import sys
from pathlib import Path


def escape_sql_string(value):
    """Escapa comillas simples para SQL."""
    if pd.isna(value) or value == "" or value is None:
        return "NULL"
    
    if isinstance(value, str):
        # Escapar comillas simples
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    
    if isinstance(value, (int, float)):
        return str(value)
    
    return f"'{str(value)}'"


def generate_products_sql(df):
    """Genera SQL para la tabla products."""
    
    sql_statements = []
    sql_statements.append("-- ============================================")
    sql_statements.append("-- INSERCIÓN DE PRODUCTOS (products)")
    sql_statements.append("-- ============================================\n")
    
    for _, row in df.iterrows():
        codigo = escape_sql_string(row.get('codigo', ''))
        nombre = escape_sql_string(row.get('nombre', ''))
        costoUnitario = row.get('costoUnitario', 0)
        ubicacion = escape_sql_string(row.get('ubicacion', 'ALMACEN PRINCIPAL'))
        salidas = row.get('salidas', 0)
        stockActual = row.get('stockActual', 0)
        stockMinimo = row.get('stockMinimo', 0)
        unidadMedida = escape_sql_string(row.get('unidadMedida', 'UND'))
        providerId = row.get('providerId', 1)
        costoTotal = row.get('costoTotal', 0)
        
        sql = f"""INSERT INTO products (codigo, nombre, "costoUnitario", ubicacion, salidas, "stockActual", "stockMinimo", "unidadMedida", "providerId", "costoTotal", "createdAt", "updatedAt")
VALUES ({codigo}, {nombre}, {costoUnitario}, {ubicacion}, {salidas}, {stockActual}, {stockMinimo}, {unidadMedida}, {providerId}, {costoTotal}, NOW(), NOW());"""
        
        sql_statements.append(sql)
    
    return "\n\n".join(sql_statements)


def generate_movement_entries_sql(df):
    """Genera SQL para la tabla movement_entries."""
    
    sql_statements = []
    sql_statements.append("\n\n-- ============================================")
    sql_statements.append("-- INSERCIÓN DE ENTRADAS (movement_entries)")
    sql_statements.append("-- ============================================\n")
    
    for _, row in df.iterrows():
        fecha = escape_sql_string(row.get('fecha', ''))
        codigoProducto = escape_sql_string(row.get('codigoProducto', ''))
        descripcion = escape_sql_string(row.get('descripcion', ''))
        precioUnitario = row.get('precioUnitario', 0)
        cantidad = row.get('cantidad', 0)
        
        sql = f"""INSERT INTO movement_entries (fecha, "codigoProducto", descripcion, "precioUnitario", cantidad, "createdAt", "updatedAt")
VALUES ({fecha}, {codigoProducto}, {descripcion}, {precioUnitario}, {cantidad}, NOW(), NOW());"""
        
        sql_statements.append(sql)
    
    return "\n\n".join(sql_statements)


def generate_movement_exits_sql(df):
    """Genera SQL para la tabla movement_exits."""
    
    sql_statements = []
    sql_statements.append("\n\n-- ============================================")
    sql_statements.append("-- INSERCIÓN DE SALIDAS (movement_exits)")
    sql_statements.append("-- ============================================\n")
    
    for _, row in df.iterrows():
        fecha = escape_sql_string(row.get('fecha', ''))
        codigoProducto = escape_sql_string(row.get('codigoProducto', ''))
        descripcion = escape_sql_string(row.get('descripcion', ''))
        precioUnitario = row.get('precioUnitario', 0)
        cantidad = row.get('cantidad', 0)
        responsable = escape_sql_string(row.get('responsable', ''))
        area = escape_sql_string(row.get('area', ''))
        proyecto = escape_sql_string(row.get('proyecto', ''))
        
        # Construir la sentencia SQL
        sql = f"""INSERT INTO movement_exits (fecha, "codigoProducto", descripcion, "precioUnitario", cantidad, responsable, area, proyecto, "createdAt", "updatedAt")
VALUES ({fecha}, {codigoProducto}, {descripcion}, {precioUnitario}, {cantidad}, {responsable}, {area}, {proyecto}, NOW(), NOW());"""
        
        sql_statements.append(sql)
    
    return "\n\n".join(sql_statements)


def main():
    """Función principal."""
    
    if len(sys.argv) < 2:
        print("Uso: python GenerateSQL.py <archivo_excel_procesado>")
        sys.exit(1)
    
    excel_file = Path(sys.argv[1])
    
    if not excel_file.exists():
        print(f"Error: El archivo {excel_file} no existe")
        sys.exit(1)
    
    print(f"Leyendo archivo: {excel_file.name}")
    
    # Leer las hojas del Excel
    df_stock = pd.read_excel(excel_file, sheet_name='Stock')
    df_entradas = pd.read_excel(excel_file, sheet_name='Entradas')
    df_salidas = pd.read_excel(excel_file, sheet_name='Salidas')
    
    print(f"\nDatos cargados:")
    print(f"  - Productos (Stock): {len(df_stock)} registros")
    print(f"  - Entradas: {len(df_entradas)} registros")
    print(f"  - Salidas: {len(df_salidas)} registros")
    
    # Generar SQL
    print("\nGenerando sentencias SQL...")
    
    sql_output = []
    
    # Header
    sql_output.append("-- ============================================")
    sql_output.append("-- SCRIPT DE INSERCIÓN DE DATOS")
    sql_output.append("-- Sistema de Inventario AYNI")
    sql_output.append("-- ============================================")
    sql_output.append("-- IMPORTANTE: Ejecutar en el orden mostrado")
    sql_output.append("-- ============================================\n")
    
    # Nota importante
    sql_output.append("-- NOTA: Asegúrate de que existe al menos un proveedor con ID=1")
    sql_output.append("-- antes de ejecutar estos inserts.\n")
    sql_output.append("-- Puedes crear uno con:")
    sql_output.append("-- INSERT INTO providers (name, email, address, phones, \"createdAt\", \"updatedAt\")")
    sql_output.append("-- VALUES ('Proveedor General', 'general@proveedor.com', 'Sin dirección', ARRAY[]::text[], NOW(), NOW());")
    sql_output.append("\n")
    
    # Generar SQL para cada tabla
    sql_output.append(generate_products_sql(df_stock))
    sql_output.append(generate_movement_entries_sql(df_entradas))
    sql_output.append(generate_movement_exits_sql(df_salidas))
    
    # Guardar en archivo
    output_file = excel_file.with_suffix('.sql')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_output))
    
    print(f"\n✅ Archivo SQL generado: {output_file}")
    print(f"Tamaño: {output_file.stat().st_size / 1024:.2f} KB")
    print(f"\nPuedes ejecutarlo en PostgreSQL con:")
    print(f"  psql -U usuario -d basededatos -f \"{output_file}\"")
    print(f"\nO copiar el contenido y pegarlo en pgAdmin o tu cliente SQL preferido.")


if __name__ == "__main__":
    main()
