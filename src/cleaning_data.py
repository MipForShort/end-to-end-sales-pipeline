import pandas as pd
import os
import glob
from sqlalchemy import create_engine
from dotenv import load_dotenv

#load_dotenv(encoding='utf-8')

CONFIG = {
    'ventas': './data/VPD/ventas_*.csv',
    'clientes': './data/clientes.csv',
    'productos': './data/productos.xlsx',
    'sucursales': './data/sucursales.csv'
}


def dataframe_ventas(ruta):
    
    # Esta linea nos guarda en una lista las rutas de cada archivo en ./data/VPD
    archivos = glob.glob(ruta)
    lista_dfs = []

    for file_name in archivos:
        df = pd.read_csv(file_name)

        # 1. Extraemos solo el nombre del archivo: ventas_01-05-2024.csv
        nombre_archivo = os.path.basename(file_name)

        # 2. Extraemos la fecha con split('_') y reemplazamos la extension '.csv'
        fecha = nombre_archivo.split('_')[1].replace('.csv', '')

        # 3. Asignamos a una columna el nuevo nombre
        df['fecha_venta'] = fecha

        # Agregamos el df a nuestra lista 
        lista_dfs.append(df)

    # Juntamos todos los dataframes en uno solo
    all_dataframes = pd.concat(lista_dfs, ignore_index= True)

    #filas_duplicadas = all_dataframes.duplicated().sum()
    #print(filas_duplicadas)

    # Reemplazamos el nombre Id a id
    #all_dataframes.rename(columns={'Id': 'id'}, inplace=True)

    # Ordenamos los indices por fecha_venta
    all_dataframes = all_dataframes.sort_values(by='fecha_venta').reset_index(drop=True)

    # No se ocupo la linea anterior, por que vamos a crear una nueva columna llamana id
    # Y la pondremos al principio del dataframe
    # Para eso, vamos a crear una nueva columna id con un range de 1 a len(all_dataframes) + 1
    # Luego con una variable cols pondremos al principio la columna id mas las demas columnas
    all_dataframes = all_dataframes.drop(columns=['Id'])
    all_dataframes['id'] = range(1, len(all_dataframes) + 1)
    cols = ['id'] + [col for col in all_dataframes.columns if col != 'id']
    all_dataframes = all_dataframes[cols]

    # Reemplazamos 'metodo_pago' por 't': 'Tarjeta', 'e': 'Efectivo'
    all_dataframes['metodo_pago'] = all_dataframes['metodo_pago'].replace({'t': 'Tarjeta', 'e': 'Efectivo'})

    # Las columnas de fecha son convertidas a datetime con su respectivo formato
    all_dataframes['fecha_venta'] = pd.to_datetime(all_dataframes['fecha_venta'], format='%d-%m-%Y')

    all_dataframes['fecha_entrega'] = pd.to_datetime(all_dataframes['fecha_entrega'], format='%Y-%m-%d')

    return all_dataframes


def dataframe_clientes(ruta):
    
    df = pd.read_csv(ruta)

    df.rename(columns={'Id': 'id',
                       'Nombre': 'nombre',
                       'Apellido': 'apellido',
                       'Correo Electrónico': 'email',
                       'País': 'pais',
                       'Teléfono': 'telefono',
                       'Dirección': 'direccion',
                       'Ciudad': 'ciudad'
                       }, inplace=True)
    
    # Quitamos todo lo que no sea digito del telefono
    df['telefono'] = df['telefono'].str.replace(r'\D', '', regex=True)

    # Revisamos si hay filas duplicadas
    #filas_duplicadas = df.duplicated().sum()
    #print(f"Filas duplicadas: {filas_duplicadas}")

    return df


def dataframe_productos(ruta):

    df = pd.read_excel(ruta, engine='openpyxl', sheet_name='productos')

    df.rename(columns={'Id': 'id',
                       'Nombre': 'nombre',
                       'Descripción': 'descripcion',
                       'Categoría': 'categoria',
                       }, inplace=True)
    
    # Revisamos si hay filas duplicadas
    #filas_duplicadas = df.duplicated().sum()
    #print(f"Filas duplicadas: {filas_duplicadas}")

    # Este df no necesitó limpieza
    return df


def dataframe_proveedores(ruta):

    df = pd.read_excel(ruta, engine='openpyxl', sheet_name='proveedores')

    df.rename(columns={'Id': 'id',
                       'Nombre': 'nombre',
                       'Contacto': 'contacto',
                       'Teléfono': 'telefono',
                       'Correo Electrónico': 'email',
                       'Dirección': 'direccion'}, inplace=True)
    
    df['telefono'] = df['telefono'].astype(str)

    # Revisamos si hay filas duplicadas
    #filas_duplicadas = df.duplicated().sum()
    #print(f"Filas duplicadas: {filas_duplicadas}")

    return df


def dataframe_sucursales(ruta):

    df = pd.read_csv(ruta)

    df.rename(columns={'dirección': 'direccion'}, inplace=True)

    # Separamos la columna ubicacion en tres columnas distintas
    df[['region', 'pais', 'ciudad']] = df['ubicacion'].str.split('/', expand=True)

    # Eliminamos la columna 'ubicacion' y 'url'
    df = df.drop(columns=['ubicacion', 'url'])

    # Reordenamos las columnas
    orden_columnas = ['id', 'nombre', 'direccion', 'encargado', 'region', 'pais', 'ciudad', 'latitud', 'longitud']
    df = df[orden_columnas]

    # Revisamos si hay filas duplicadas
    #filas_duplicadas = df.duplicated().sum()
    #print(f"Filas duplicadas: {filas_duplicadas}")

    return df


if __name__ == '__main__':
    
    ventas = dataframe_ventas(CONFIG['ventas'])
    print(ventas.info())

    clientes = dataframe_clientes(CONFIG['clientes'])
    print(clientes.info())

    productos = dataframe_productos(CONFIG['productos'])
    print(productos.info())

    proveedores = dataframe_proveedores(CONFIG['productos'])
    print(proveedores.info())

    sucursales = dataframe_sucursales(CONFIG['sucursales'])
    print(sucursales.info())
