import os
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Archivos como variables
DATA_PATH=#"Coloca la ruta de acceso dónde colocaste las fuentes de datos"
FILE_BRASIL_GEODATA = 'brasil_geodata.json'
FILE_BRASIL_REGIONS = 'brasil_regions.csv'
FILE_CUSTOMERS = 'olist_customers_dataset.xlsx'
FILE_GEOLOCATIONS = 'olist_geolocation_dataset.csv'
FILE_ITEMS = 'olist_order_items_dataset.csv'
FILE_PAYMENTS = 'olist_order_payments_dataset.csv'
FILE_ORDERS = 'olist_orders_dataset.csv'
FILE_STATES_ABBREVIATIONS = 'states_abbreviations.json'

# Lectura de archivos
brasil_geodata = pd.read_json(
    os.path.join(DATA_PATH, FILE_BRASIL_GEODATA)
)
brasil_regions = pd.read_csv(
    os.path.join(DATA_PATH, FILE_BRASIL_REGIONS)
)
customers = pd.read_excel(
    os.path.join(DATA_PATH, FILE_CUSTOMERS),
    dtype={'customer_zip_code_prefix': str}
    )
geolocations = pd.read_csv(
    os.path.join(DATA_PATH, FILE_GEOLOCATIONS),
    dtype={'geolocation_zip_code_prefix': str}
    )
items = pd.read_csv(
    os.path.join(DATA_PATH, FILE_ITEMS)
    )
payments = pd.read_csv(
    os.path.join(DATA_PATH, FILE_PAYMENTS)
    )
states_abbreviations = pd.read_json(
    os.path.join(DATA_PATH, FILE_STATES_ABBREVIATIONS)
    )
orders = pd.read_csv(
    os.path.join(DATA_PATH, FILE_ORDERS)
    )

# Conversión de columnas en formato fecha
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'] , errors='coerce' )
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'] , errors='coerce' )
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'] , errors='coerce' )
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'] , errors='coerce' )
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'] , errors='coerce' )

# Variables auxiliares con año, mes y trimestre del año que se realizó la orden
orders['year'] = orders['order_purchase_timestamp'].dt.year
orders['month'] = orders['order_purchase_timestamp'].dt.month
orders['quarter'] = orders['order_purchase_timestamp'].dt.to_period('Q')
orders['year_month'] = orders['order_purchase_timestamp'].dt.to_period('M')

# Calculo de tiempo de entregas
orders['delta_days'] = (
    orders['order_delivered_customer_date'] -
    orders['order_estimated_delivery_date']
    ).dt.total_seconds()/ 60 / 60 / 24
# Identificación de status de entrega
orders['delay_status']  = np.where(
    orders['delta_days'] > 3, 'long_delay',
    np.where(orders['delta_days'] <= 0, 'on_time','short_delay')
    )

# variable auxiliar para conteo de productos y suma de precio de articulos.
items_agg = items.groupby(
    ['order_id']).agg(
        {'order_item_id': 'count', # conteo de producto
        'price': 'sum'} # suma de los precios de los artículos
                      ).reset_index() 
# Cambio de nombre en columnas
items_agg.rename(
    columns={'order_item_id': 'total_products', 'price': 'total_sales'},
    inplace=True
    )

# Corrección de información redundante en códigos posatales
unique_geolocations = geolocations.drop_duplicates(
    subset = ['geolocation_zip_code_prefix']
    )

# Consolidación de tablas
customers_geolocation = customers.merge(
    unique_geolocations,
    left_on='customer_zip_code_prefix',
    right_on='geolocation_zip_code_prefix',
    how='left'
)
customers_geolocation_estado = customers_geolocation.merge(
    states_abbreviations,
    left_on='geolocation_state',
    right_on='abbreviation',
    how='left'
)
orders_totals = orders.merge(
    items_agg,
    left_on=['order_id'],
    right_on=['order_id'],
    how='left'
    )
results = orders_totals.merge(
    customers_geolocation_estado,
    left_on=['customer_id'],
    right_on=['customer_id'],
    how='left'
    )

# Guardar la tabla consolidada en archivo .csv
results.to_csv('oilst_processed.csv', index=False)
