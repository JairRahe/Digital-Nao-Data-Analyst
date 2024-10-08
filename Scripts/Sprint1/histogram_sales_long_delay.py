import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Archivos como variables
DATA_PATH="/Users/Pedro Ramirez/OneDrive - Hospitales MAC/Documents/Sprint1/results"
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

# Figura
fig, ax = plt.subplots(figsize=(5, 3))
n_bins = 100

# Creacion del historgama
n, bins, patches = ax.hist(
    delivered['total_sales'],
    n_bins
    )
ax.set_title('Histograma de frequencias de total_sales y regla empírica débil' )
ax.set_xlabel('Total de ventas')
ax.set_ylabel('Frecuencia')

## Media y regiones de regla empirica debil
plt.axvline(
    delivered['total_sales'].mean(),
    color='r',
    linestyle='dashed',
    linewidth=3)

plt.axvline(
    delivered['total_sales'].mean() + 3*delivered['total_sales'].std(),
    color='y',
    linestyle='dashed',
    linewidth=2)

plt.axvline(
    delivered['total_sales'].mean() - 3*delivered['total_sales'].std(),
    color='y',
    linestyle='dashed',
    linewidth=2)

## limites de la figura
min_ylim, max_ylim = plt.ylim()

## Etiquetas
plt.text(
    delivered['total_sales'].mean()*1.1,
    max_ylim*0.9,
    'Promedio: {:.2f}'.format(delivered['total_sales'].mean())
    )

plt.savefig("histogram_sales_long_delay.png")
plt.show()
