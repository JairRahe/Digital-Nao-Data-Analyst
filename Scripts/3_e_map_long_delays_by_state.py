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

#Agrupar retrasos por estado
grouped_delays_by_state = delivered.query(
    "delay_status == 'long_delay'"
    ).groupby(['state_name', 'geolocation_state'])['delay_status'].count().reset_index()

#Creación de mapa interactivo
fig = px.choropleth(
    data_frame=grouped_delays_by_state,
    geojson=geojson,
    featureidkey='properties.UF',
    # featureidkey='properties.ESTADO',
    locations='geolocation_state',
    color='delay_status',
    # https://plotly.com/python/builtin-colorscales/
    color_continuous_scale="bluyl",
    scope='south america',
    labels={'delay_status': 'Cantidad de pedidos retrasados'},
    width=800,
    height=400,
    title="Mapa de la cantidad de órdenes con entregas de restraso prolongado a nivel estatal"
)

#Actualizar diseño de la figura
fig.update_geos(
    showcountries=False,
    showcoastlines=True,
    showland=True,
    fitbounds='locations',
    visible=True
)

fig.update_layout(
    margin=dict(l=20, r=20, t=66, b=20),
    width=800,
    height=800,
)

# Guardar el mapa como HTML
fig.write_html('3_e_map_long_delays_by_state.html')
