import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#Lectura de datos
DATA_PATH="/Users/Pedro Ramirez/OneDrive - Hospitales MAC/Documents/Sprint1/data"
FILE_CONSOLIDATED_DATA = 'oilst_processed.csv'

#Conversión de fechas
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

#Filtros de entregas completadas, con entregas moderadas y prolongadas
delivered = oilst.query("order_status == 'delivered'")
delivered_moderado = delivered[delivered['delay_status'] == 'short_delay']
delivered_prolongado = delivered[delivered['delay_status'] == 'long_delay']

# Crear los histogramas
plt.figure(figsize=(10, 6))
sns.histplot(data=delivered_moderado, x='total_sales', bins=20, color='blue', label='Retraso Moderado', kde=True)
sns.histplot(data=delivered_prolongado, x='total_sales', bins=20, color='red', label='Retraso Prolongado', kde=True)
plt.title('Comparación de ventas de retrasos moderados vs prolongados')
plt.xlabel('Valor de Venta')
plt.ylabel('Número de Órdenes')
plt.legend()

# Guardar imagen como png
plt.savefig('3_a_histogram_sales_short_long_delays.png')
plt.show()
