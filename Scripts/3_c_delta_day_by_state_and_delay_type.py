import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#Lectura de datos.
DATA_PATH=#"Coloca la ruta de acceso dónde colocaste las fuentes de datos"
FILE_CONSOLIDATED_DATA = 'oilst_processed.csv'

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

#Filtros de entregas completadas, con entregas moderadas y prolongadas.
delivered = oilst.query("order_status == 'delivered'")

# Crear la figura para la visualización.
plt.figure(figsize=(14, 8))

# Visualización de la distribución de la variable delta_days a lo largo de los estados de Brasil.
sns.boxplot(x='customer_state', y='delta_days', hue='delay_status', data=delivered)
plt.title('Distribución de Delta Days por Estado y Tipo de Retraso')
plt.xlabel('Estado')
plt.ylabel('Delta Days')

# Rotar las etiquetas del eje x para una mejor legibilidad.
plt.xticks(rotation=45)

# Guardar la imagen.
plt.savefig('3_c_delta_day_by_state_and_delay_type.png')
plt.show()
