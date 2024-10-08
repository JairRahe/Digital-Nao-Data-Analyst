import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Archivos como variables
DATA_PATH= #"Coloca la ruta de acceso a la carpeta dónde colocaste las fuentes de datos"
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

#Filtro por estado entregado y mayor a 10 días de atraso
delivered_filter = "order_status  == 'delivered'"
delay_filter = "delta_days > 10"
delivered = oilst.query(delivered_filter)
delivered_delta = delivered.query(delay_filter)

corr_matrix=delivered_delta[
    ['total_sales', 'total_products', 'distance_distribution_center', 'delta_days']
    ].corr().round(4)

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Matriz de Correlación - Órdenes con Retraso Mayor a 10 Días')
plt.savefig("correlation_matrix_10_days_delay.png")
plt.show()

