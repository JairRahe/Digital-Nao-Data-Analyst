# Análisis de Datos de Olist

Este repositorio contiene los scripts necesarios para realizar un análisis de las ventas de productos del E-comerce OLIST

## Estructura del Repositorio

* **scripts:** Contiene los scripts de Python para el procesamiento y análisis de datos.

## Descripción de los Scripts

* **1_1_oilst_processed.py:** 
  * Carga y procesa las diferentes fuentes de datos del e-commerce.
  * Crea una tabla consolidada que servirá como base para los análisis posteriores.
* **prop_sales_delay_status_by_quarte.py:** 
  * Calcula la proporción de ventas de órdenes completas de Oilst por categoría de retraso y trimestre (2016-2018).
  * Genera el archivo "prop_sales_delay_status_by_quarte.csv".
* **count_orders_basket_size_by_delay_status.py:** 
  * Cuenta el número de órdenes por cantidad de productos y categoría de retraso.
  * Genera el archivo "count_orders_basket_size_by_delay_status.csv".
* **histogram_sales_long_delay.py:** 
  * Crea un histograma de las ventas totales para órdenes completas aplicando la regla empírica débil para identificar el 88.88% de los datos alrededor de la media.
  * Genera la figura "histogram_sales_long_delay.png".
* **correlation_matrix_10_days_delay.py:** 
  * Calcula la matriz de correlación entre variables clave para órdenes con retrasos superiores a 10 días.
  * Genera la figura "correlation_matrix_10_days_delay.png".

## Cómo Utilizar Este Repositorio

1. **Requisitos previos**

   **Python:** Asegúrate de tener Python instalado en tu sistema. Puedes descargar la última versión desde https://www.python.org/downloads/
   
   **Bibliotecas de python:** Deberas instalar las bibliotecas necesarias para la ejecución de los scripts, para ello podras abrir tu terminal y ejecutar los siguientes comandos:
   ```
   pip install pandas
   pip install numpy
   pip install seaborn
   pip install matplotlib
   ```
   
3. **Descarga de funtes de datos**
   
   Puedes descargar los datos utilizados desde https://drive.google.com/drive/folders/1-qAQto59pNOxtADZuitZp0odSsLPM3l6
   
> [!NOTE]
> Es importante que organices en una carpeta todos los archivos descargados para facilitar el procasimiento de los mismos.
   
3.  **Descargar el repositorio:**
   
4.  **Ejecutar los scripts**
   
   scripts/1_1_oilst_processed.py
   
   scripts/prop_sales_delay_status_by_quarte.py
   
 ... y así sucesivamente para los demás scripts
    
> [!CAUTION]
> Antes de ejecutar cada script, revisa la variable **DATA_PATH**, deberas colocar la ruta de acceso a la carpeta dónde guardaste las fuentes de datos.
 

## Resultados Esperados
Los resultados de los análisis se encuentran en la carpeta results. Estos resultados pueden utilizarse para:

* Identificar patrones en los retrasos de entrega.
* Analizar el impacto del tamaño del pedido en los retrasos.
* Evaluar la relación entre las ventas y otras variables como la distancia al centro de distribución.
