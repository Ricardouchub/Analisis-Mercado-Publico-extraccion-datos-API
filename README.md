# Detección de anomalías en el Mercado Público de Chile


<p align="left"> 
  <img src="https://img.shields.io/badge/Proyecto_en_Proceso-%F0%9F%94%8B-F1C40F?style=flat-square&logo=progress&logoColor=white" alt="Proyecto en Proceso"/>
  <a href="https://aws.amazon.com" target="blank">
    <img src="https://img.shields.io/badge/AWS-Cloud-232F3E?style=flat-square&logo=amazonaws&logoColor=white" alt="AWS"/></a>
  <a href="https://aws.amazon.com/lambda/" target="blank">
    <img src="https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat-square&logo=aws-lambda&logoColor=white" alt="AWS Lambda"/></a>
  <a href="https://aws.amazon.com/s3/" target="blank">
    <img src="https://img.shields.io/badge/AWS-S3-569A31?style=flat-square&logo=amazons3&logoColor=white" alt="Amazon S3"/></a>
  <a href="https://aws.amazon.com/eventbridge/" target="blank">
    <img src="https://img.shields.io/badge/AWS-EventBridge-EF3422?style=flat-square&logo=amazonaws&logoColor=white" alt="Amazon EventBridge"/></a>
  <a href="https://www.python.org" target="blank">
    <img src="https://img.shields.io/badge/Python-3.9-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://requests.readthedocs.io/" target="blank">
    <img src="https://img.shields.io/badge/Requests-HTTP-E44D40?style=flat-square&logo=python&logoColor=white" alt="Requests"/></a>
  <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html" target="blank">
    <img src="https://img.shields.io/badge/Boto3-Client-007AFF?style=flat-square&logo=amazonaws&logoColor=white" alt="Boto3"/></a>
</p>


Este proyecto busca identificar patrones de compra inusuales y potenciales "red flags" dentro de los datos de Mercado Público de Chile. El objetivo es desarrollar un sistema de análisis que pueda alertar sobre transacciones con características atípicas, tales como licitaciones con un único oferente, adjudicaciones por montos cercanos al máximo presupuestado, o la concentración de contratos en proveedores nuevos.

El proyecto está dividido en dos fases principales:

* **Fase 1: Ingesta de datos** - Construcción de un pipeline automatizado para la recolección de datos.
* **Fase 2: Análisis de datos** - Exploración y modelado de los datos para la detección de anomalías.

---
## Fase 1: Pipeline de Datos en AWS

Durante la exploración inicial, se descubrió una limitación crítica en la API de Mercado Público: **el endpoint no permite realizar consultas para fechas pasadas de manera fiable**, devolviendo errores al intentar acceder a datos históricos. La API está diseñada para entregar únicamente datos muy recientes (de las últimas 24-48 horas).

Para superar este obstáculo, en lugar de una extracción masiva única, se diseñó y construyó un **pipeline de datos diario y automatizado** en Amazon Web Services (AWS). Esta solución recolecta los datos cada día y los almacena de forma incremental, construyendo un dataset histórico a lo largo del tiempo.

### Arquitectura del Pipeline

El siguiente diagrama ilustra el flujo de trabajo automatizado:

<img width="830" height="501" alt="image" src="https://github.com/user-attachments/assets/ad28845d-2909-4ef9-b959-849e2ae47374" />



---
## Cómo Reproducir la Pipeline

**Prerrequisitos:**

* Una cuenta de AWS con permisos para crear recursos en IAM, S3, Lambda y EventBridge.

* Un "Ticket" (API Key) válido de la API de Mercado Público.

**Crear un Bucket en S3:** Configura un bucket de S3 que servirá como el almacén para los archivos CSV diarios.

**Desplegar la Función Lambda:**

* Crea un Rol de IAM con los permisos necesarios (AWSLambdaBasicExecutionRole y AmazonS3FullAccess).

* Crea la primera función Lambda utilizando el script `lambda_function_licitaciones.py`.
* Crea la segunda función Lambda utilizando el script `lambda_function_ordenescompra.py`.

**Importante:**

Antes de desplegar, debes modificar las siguientes variables en el script con tus propios valores al principio del script:

`# Reemplaza con el nombre de tu bucket`

`NOMBRE_BUCKET = "NOMBRE_DE_TU_BUCKET_S3"`

`# Tu ticket de la API`

`MI_TICKET = "TICKET_DE_LA_API"`

**Automatizar con EventBridge:** 

Crea una regla de programación en Amazon EventBridge que active la función Lambda diariamente en el horario que prefieras.

**Puedes probar el funcionamiento correcto de la API y de tu API Key con el notebook de la carpeta `prueba local`**

---

## Fase 2: Análisis de Datos y Detección de Anomalías (en proceso)
(Esta sección se completará a medida que se obtengan datos para poder determinar el flujo del pipeline)

Una vez que el pipeline haya recolectado un volumen de datos suficiente, se procederá a:

Carga y Limpieza: Leer los archivos CSV diarios desde S3, unificarlos en un solo DataFrame y realizar la limpieza y preprocesamiento de los datos.

Análisis Exploratorio (EDA): Investigar las distribuciones, identificar proveedores y organismos con mayor actividad, y analizar la frecuencia de los tipos de compra.

Detección de anomalías: Aplicar reglas de negocio y modelos estadísticos para identificar red flags.

---

## Estructura del Repositorio

* **`lambda_function_licitaciones.py`** Script para recolección de licitaciones desde la API.
* **`lambda_function_ordenescompra.py`** Script para recolección de ordenes de compra desde la API.
* **`requeriments.txt`**
* **`/prueba local/`** Carpeta que contiene un notebook para hacer una prueba local de la API y de la API Key obtenida.

---
## Autor

**Ricardo Urdaneta**

[LinkedIn](https://www.linkedin.com/in/ricardourdanetacastro)
