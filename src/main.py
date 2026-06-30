import pandas as pd
import os
import etl_functions as etl
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv(encoding='utf-8')


def get_db_engine():
    # String for creating the engine
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db = os.getenv('DB_NAME')

    print("Database Connection")
    print(f"User: {user}, Port: {port}\n")

    # Return the engine
    return f'postgresql://{user}:{password}@{host}:{port}/{db}'


DB_URL = get_db_engine()
engine = create_engine(DB_URL)


def inicializar_base_de_datos():
    """Ejecuta el script SQL para crear las tablas si no existen."""
    print("--- Inicializando esquema de base de datos ---")
    try:
        with open('src/schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        with engine.connect() as conn:
            # Ejecutamos el script completo
            conn.execute(text(sql_script))
            conn.commit() # Asegura que los cambios se guarden
        print("Esquema creado/verificado correctamente.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")


def run_pipeline():
    # 1. Primero creamos las tablas

    inicializar_base_de_datos()

    print("--- Iniciando ETL Pipeline ---")
    # 2. Extracción y Transformación
    ventas = etl.dataframe_ventas(etl.CONFIG['ventas'])
    clientes = etl.dataframe_clientes(etl.CONFIG['clientes'])
    productos = etl.dataframe_productos(etl.CONFIG['productos'])
    proveedores = etl.dataframe_proveedores(etl.CONFIG['productos'])
    sucursales = etl.dataframe_sucursales(etl.CONFIG['sucursales'])
    prods_prov = etl.dataframe_productos_proveedor(etl.CONFIG['productos_proveedor'])
    pais = etl.dataframe_pais_url(etl.CONFIG['pais_url'])

    # Solo dejamos las ventas cuyos IDs existan en las tablas maestras
    ventas = ventas[ventas['producto_id'].isin(productos['id'])]
    ventas = ventas[ventas['sucursal_id'].isin(sucursales['id'])]
    ventas = ventas[ventas['cliente_id'].isin(clientes['id'])]

    # 3. Carga a SQL (Orden estricto por Foreign Keys)
    data_to_load = [
        ('paises', pais),
        ('productos', productos),
        ('sucursales', sucursales),
        ('clientes', clientes),
        ('proveedores', proveedores),
        ('productos_proveedores', prods_prov),
        ('ventas', ventas)
    ]

    for nombre_tabla, df in data_to_load:
        if not df.empty:
            df.to_sql(nombre_tabla, engine, if_exists='append', index=False)
            print(f"Tabla '{nombre_tabla}' cargada exitosamente.")
        else:
            print(f"Advertencia: Tabla '{nombre_tabla}' está vacía. Saltando carga.")


if __name__ == '__main__':
    run_pipeline()