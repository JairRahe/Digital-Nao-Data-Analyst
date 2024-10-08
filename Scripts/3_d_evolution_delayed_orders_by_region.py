#Importar las librerias a usar
import os
import json
import plotly.express as px
import numpy as np
import pandas as pd

#Lectura de datos.
DATA_PATH=#"Coloca la ruta de acceso dónde colocaste las fuentes de datos"
FILE_CONSOLIDATED_DATA = 'oilst_processed.csv'
FILE_GEODATA = 'brasil_geodata.json'
FILE_REGIONS = 'brasil_regions.csv'

#Carga de datos geograficos de brasil
with open(os.path.join(DATA_PATH, FILE_GEODATA), 'r') as f:
    geojson = json.load(f)
regions = pd.read_csv(
    os.path.join(DATA_PATH, FILE_REGIONS),
)

#Conversión de fechas.
columns_dates=[
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
    ]
oilst = pd.read_csv(
    os.path.join(DATA_PATH, FILE_CONSOLIDATED_DATA),
    parse_dates=columns_dates
    )

#Creación de columna de región de brasil
oilst = oilst.merge(regions[['abbreviation', 'region']], on='abbreviation', how='left')

#Mayusculas al inicio de los nombres de ciudades
oilst['geolocation_city'] = oilst['geolocation_city'].str.title()

#Filtro de las ordenes completadas
delivered = oilst.query("order_status == 'delivered'")

#Agrupación de los datos por mes, año y región, contando los retrasos prolongados
delayed_orders = delivered[delivered['delay_status'] == 'long_delay'].groupby(['year_month', 'geolocation_state']).size().reset_index(name='count')

#Creación del grafico de barras interactivo
fig = px.bar(
    delayed_orders,
    x='year_month',
    y='count',
    color='geolocation_state',
    title='Órdenas con Retraso prolongado por cada mes, año y región',
    labels={'year_month': 'Mes y Año', 'count': 'Cantidad de Órdenes'},
    hover_name='geolocation_state'
)

#Guardar la figura como HTML
fig.write_html('3_d_evolution_delayed_orders_by_region.html')
