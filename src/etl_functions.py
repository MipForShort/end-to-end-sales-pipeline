import pandas as pd
import os
import glob
import tabula
import requests
from bs4 import BeautifulSoup


CONFIG = {
    'ventas': './data/VPD/ventas_*.csv',
    'clientes': './data/clientes.csv',
    'productos': './data/productos.xlsx',
    'sucursales': './data/sucursales.csv',
    'productos_proveedor': './data/productos_proveedor.pdf',
    'pais_url': './data/url.txt'
}


def dataframe_ventas(ruta: str):
    try:
        # Esta linea nos guarda en una lista las rutas de cada archivo en ./data/VPD
        archivos = glob.glob(ruta)

        # Validamos que archivos no este vacio
        if not archivos:
            print("No se encontraron archivos en la ruta especificada.")
            return pd.DataFrame()
        
        lista_dfs = []

        for file_name in archivos:

            df = cargar_archivo(file_name)

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
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error inesperado: {e}")
        return pd.DataFrame()


def dataframe_clientes(ruta: str):
    try:
        df = cargar_archivo(ruta)

        # Renombramos las columnas
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
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error inesperado: {e}")
        return pd.DataFrame()


def dataframe_productos(ruta: str):
    try:
        if ruta.endswith(".csv"):
            df = pd.read_csv(ruta)
        elif ruta.endswith(".xlsx"):
            df = pd.read_excel(ruta, engine='openpyxl', sheet_name='productos')

        # Renombramos las columnas 
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
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error inesperado: {e}")
        return pd.DataFrame()


def dataframe_proveedores(ruta: str):
    try:
        if ruta.endswith(".csv"):
            df = pd.read_csv(ruta)
        elif ruta.endswith(".xlsx"):
            df = pd.read_excel(ruta, engine='openpyxl', sheet_name='proveedores')

        # Renombramos las columnas
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
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error inesperado: {e}")
        return pd.DataFrame()


def dataframe_sucursales(ruta: str):
    try:
        df = cargar_archivo(ruta)

        # Renombramos las columnas
        df.rename(columns={'dirección': 'direccion'}, inplace=True)

        # Separamos la columna ubicacion en tres columnas distintas
        df[['region', 'pais', 'ciudad']] = df['ubicacion'].str.split('/', expand=True)

        # Eliminamos la columna 'ubicacion' y 'url'
        df = df.drop(columns=['ubicacion', 'url'], errors='ignore')

        # Reordenamos las columnas
        orden_columnas = ['id', 'nombre', 'direccion', 'encargado', 'region', 'pais', 'ciudad', 'latitud', 'longitud']
        df = df[orden_columnas]

        # Revisamos si hay filas duplicadas
        #filas_duplicadas = df.duplicated().sum()
        #print(f"Filas duplicadas: {filas_duplicadas}")

        return df
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error inesperado: {e}")
        return pd.DataFrame()


def dataframe_productos_proveedor(ruta: str):
    try:
        # Leemos un archivo pdf con la ruta de nuestro CONFIG
        df = cargar_archivo(ruta)

        # Renombramos las columnas
        df.rename(columns={'días_entrega': 'dias_entrega'}, inplace=True)

        # Eliminamos duplicados
        df = df.drop_duplicates(subset=['producto_id', 'proveedor_id'])

        return df
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error inesperado: {e}")
        return pd.DataFrame()


def dataframe_pais_url(ruta: str):
    try:
        with open(ruta, "r") as file:
            url = file.readline().strip()
            
        # Usamos requests para obtener el HTML
        response = requests.get(url)
        response.raise_for_status() # Lanza error si la web no responde bien
        
        # Usamos BeautifulSoup para extraer la tabla
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="table table-bordered downloads tablesorter")
        
        # Convertimos la tabla HTML a una lista de listas de forma eficiente
        headers = [th.text.strip() for th in table.find_all("th")]
        rows = []
        for tr in table.find_all("tr")[1:]: # Saltar header
            cells = [td.text.strip() for td in tr.find_all("td")]
            if cells:
                rows.append(cells)
        
        # Crear DataFrame directamente
        df = pd.DataFrame(rows, columns=headers)

        # Limpieza
        df = df.drop(columns=['Alpha-3 code', 'Numeric'], errors='ignore')
        df.rename(columns={'Country': 'pais', 'Alpha-2 code': 'codigo'}, inplace=True)

        return df
    except Exception as e:
        print(f"Error inesperado: {e}")
        return pd.DataFrame()


def cargar_archivo(ruta: str):
    if ruta.endswith(".csv"):
        return pd.read_csv(ruta)
    elif ruta.endswith(".xlsx"):
        return pd.read_excel(ruta, engine="openpyxl")
    elif ruta.endswith(".pdf"):
        # Tabula devuelve una lista, tomamos la primera tabla
        return tabula.read_pdf(ruta, pages="all")[0]
    else:
        raise ValueError(f"Formato no soportado: {ruta}")
    

if __name__ == '__main__':
    
    ventas = dataframe_ventas(CONFIG['ventas'])
    print("Ventas")
    print(ventas.info())
    #print(ventas.head())
    #print()

    clientes = dataframe_clientes(CONFIG['clientes'])
    print("Clientes")
    print(clientes.info())
    #print(clientes.head())
    #print()

    productos = dataframe_productos(CONFIG['productos'])
    print("Productos")
    print(productos.info())
    #print(productos.head())
    #print()

    proveedores = dataframe_proveedores(CONFIG['productos'])
    print("Proveedores")
    print(proveedores.info())
    #print(proveedores.head())
    #print()

    sucursales = dataframe_sucursales(CONFIG['sucursales'])
    print("Sucursales")
    print(sucursales.info())
    #print(sucursales.head())
    #print()

    productos_proveedor = dataframe_productos_proveedor(CONFIG['productos_proveedor'])
    print("Productos-Proveedor")
    print(productos_proveedor.info())
    #print(productos_proveedor.head())
    #print()

    pais = dataframe_pais_url(CONFIG['pais_url'])
    print("Pais")
    print(pais.info())
    #print(pais.head())
    #print()

