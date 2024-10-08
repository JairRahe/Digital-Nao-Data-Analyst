import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

# Filtrar datos para órdenes completas
delivered_filter = "order_status  == 'delivered' "
delivered = oilst.query(delivered_filter)

# Creación de tabla con proporción de ventas segun el estado de retraso por trimestre.
prop_sales = delivered.pivot_table(
    index='delay_status',
    columns = 'quarter',
    values= 'total_sales',
    aggfunc= 'sum',
    margins=True,
    fill_value=0
    ).apply(lambda x: x / float(x.sum()), axis=0).round(2)

# Guardar la tabla creada en archivo .csv
prop_sales.to_csv('prop_sales_delay_status_by_quarte.csv', index=True)
