import json
import requests
import pandas as pd
import boto3
from datetime import datetime
import os

def lambda_handler(event, context):
    """
    Función Lambda que obtiene las ÓRDENES DE COMPRA de la API 
    y las guarda en un nuevo archivo CSV diario en un bucket de S3.
    """
    # Cargar configuración desde variables de entorno 
    NOMBRE_BUCKET = os.environ.get('NOMBRE_S3_BUCKET')
    MI_TICKET = os.environ.get('CAMBIAR_POR_TU_KEY_AQUI')
    
    # Generar el nombre del archivo
    fecha_hoy_str = datetime.now().strftime('%Y-%m-%d')
    nombre_archivo = f"ordenes_de_compra/oc_{fecha_hoy_str}.csv"
    
    print(f"Iniciando recolección para el archivo: {nombre_archivo}")

    # Consultar la API de Órdenes de Compra
    url_api = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?ticket={MI_TICKET}"
    response = requests.get(url_api, timeout=60)
    
    if response.status_code != 200:
        print(f"Error al consultar la API: {response.status_code}. Abortando.")
        return {'statusCode': 500, 'body': json.dumps('Error en la API externa')}

    # Procesar los datos
    df_nuevos = pd.DataFrame(response.json().get('Listado', []))
    
    if df_nuevos.empty:
        print("No se encontraron nuevas órdenes de compra. Finalizando.")
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