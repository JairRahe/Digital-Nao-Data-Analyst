import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Archivos como variables
DATA_PATH=#"Coloca la ruta de acceso dónde colocaste las fuentes de datos"
FILE_CONSOLIDATED_DATA = 'oilst_processed.csv'

# Lectura de datos con columnas consideradas como fechas
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

# Agrupar por tamaño de canasta y tipo de retraso, contando las órdenes
result = oilst.groupby(['total_products', 'delay_status']).size().reset_index(name='order_count')

# Guardar el resultado en un nuevo archivo CSV
result.to_csv('count_orders_basket_size_by_delay_status.csv', index=False)