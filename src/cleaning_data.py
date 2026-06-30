import pandas as pd
import os
import glob
from sqlalchemy import create_engine
from dotenv import load_dotenv

#load_dotenv(encoding='utf-8')

def dataframe_ventas():
    # Esta linea nos guarda en una lista las rutas de cada archivo en ./data/VPD
    archivos = glob.glob('./data/VPD/ventas_*.csv')
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

    all_dataframes = pd.concat(lista_dfs, ignore_index= True)

    #filas_duplicadas = all_dataframes.duplicated().sum()
    #print(filas_duplicadas)

    # Reemplazamos el nombre Id a id
    #all_dataframes.rename(columns={'Id': 'id'}, inplace=True)

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

    # Vemos como va el proceso
    #print(all_dataframes.head(5))
    #print(all_dataframes.info())

    return all_dataframes


if __name__ == '__main__':
    ventas = dataframe_ventas()
    print(ventas.info())
    print(ventas.head())

