import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#Lectura de datos
DATA_PATH=#"Coloca la ruta de acceso dónde colocaste las fuentes de datos"
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

# Seleccionar solo las columnas numéricas
var_number = delivered.select_dtypes(include=['number']).columns

# Calcular la matriz de correlación
corr_matrix = delivered[var_number].corr()

# Crear el heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Matriz de Correlación para Órdenes Completadas')
plt.savefig('3_b_correlation_matrix_complete_orders.png')
plt.show()
