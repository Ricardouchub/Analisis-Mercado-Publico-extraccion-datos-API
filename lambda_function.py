import json
import requests
import pandas as pd
import boto3 # SDK de AWS para Python
from datetime import datetime

# --- CONFIGURACIÓN ---
# Reemplaza con el nombre de tu bucket
NOMBRE_BUCKET = "NOMBRE_S3_BUCKET" 
# Tu ticket de la API
MI_TICKET = "CAMBIAR_POR_TU_KEY_AQUI" 

def lambda_handler(event, context):
    """
    Función Lambda que obtiene datos de la API de Mercado Público
    y los guarda en un nuevo archivo CSV diario en un bucket de S3.
    """
    # Generar el nombre del archivo con la fecha de hoy
    fecha_hoy_str = datetime.now().strftime('%Y-%m-%d')
    # Guardaremos los archivos en una "carpeta" dentro del bucket
    nombre_archivo = f"licitaciones/licitaciones_{fecha_hoy_str}.csv"
    
    print(f"Iniciando recolección para el archivo: {nombre_archivo}")

    # Consultar la API de Mercado Público
    url_api = f"https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?ticket={MI_TICKET}"
    response = requests.get(url_api, timeout=60)
    
    if response.status_code != 200:
        print(f"Error al consultar la API: {response.status_code}. Abortando.")
        return {'statusCode': 500, 'body': json.dumps('Error en la API externa')}

    # Procesar los datos con pandas
    df_nuevos = pd.DataFrame(response.json().get('Listado', []))
    
    if df_nuevos.empty:
        print("No se encontraron nuevas licitaciones. Finalizando.")
        return {'statusCode': 200, 'body': json.dumps('No hay datos nuevos')}

    # Inicializar el cliente de S3
    s3_client = boto3.client('s3')

    # Convertir el DataFrame a formato CSV en memoria
    csv_buffer = df_nuevos.to_csv(index=False)
    
    # Subir el archivo CSV al bucket de S3
    s3_client.put_object(
        Bucket=NOMBRE_BUCKET,
        Key=nombre_archivo,
        Body=csv_buffer
    )
    
    print(f"Proceso completado. {len(df_nuevos)} registros guardados en '{nombre_archivo}'.")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Archivo {nombre_archivo} guardado exitosamente!')
    }