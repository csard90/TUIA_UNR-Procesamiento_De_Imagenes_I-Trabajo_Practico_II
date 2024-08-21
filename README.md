# TP2 Procesamiento de Imágenes

## Instrucciones para ejecutar el Trabajo Práctico

Este repositorio contiene dos archivos de Python, "Problema_1.py" y "Problema_2.py", que se utilizan para la resolución de las consignas solicitadas en el Trabajo Práctico Nº 2. También contiene un directorio empleado para almacenar las imágenes requeridas en cada uno de los problemas. 

A continuación, se detallan los pasos para ejecutar estos archivos en su entorno de desarrollo.

## Requisitos Previos

Antes de ejecutar los archivos, asegúrate de tener instalado Python en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/) e instalarlo siguiendo las instrucciones correspondientes a tu sistema operativo.

Además, es posible que necesites instalar algunas bibliotecas Python adicionales. Puedes hacerlo utilizando el administrador de paquetes `pip`. Ejecuta los siguientes comandos para instalar las bibliotecas necesarias (OpenCV - MathPlotLib - Numpy):

`pip install opencv-contrib-python matplotlib numpy`

## Ejecución del Problema_1

El archivo "Problema_1.py" realiza una detección y clasificación de monedas y dados en una imagen. Para ejecutarlo, siga estos pasos:

* Asegúrese de que la imagen de entrada esté en la carpeta "Imagenes" ya que se utilizará la dirección relativa para acceder a esta. Cambie el nombre de la imagen o ajuste la ruta en el archivo si es necesario.

* Abra una terminal o línea de comandos en el directorio donde se encuentra "Problema_1.py".

* Ejecute el siguiente comando para ejecutar el script:
`python Problema_1.py`
  
El resultado se mostrará en una ventana de gráficos y se cerrará cuando usted cierre la propia ventana.


## Ejecución del Problema_2

El archivo "Problema_2.py" se utiliza para detectar patentes en los vehículos. Para ejecutarlo, siga estos pasos:

* Asegúrese de que las imágenes de entrada estén en la carpeta "Imagenes" ya que se utilizará la dirección relativa para acceder a ellas. Puede cambiar los nombres de las imágenes o ajustar la ruta en el archivo si es necesario.

* Abra una terminal o línea de comandos en el directorio donde se encuentra "Problema_2.py".

* Ejecute el siguiente comando para ejecutar el script:
`python Problema_2.py`

El script procesará cada una de las imágenes y mostrará una a una la imagen original con el recuadro de la patente detectada, para ir pasando de imagen en imagen, tiene que cerrar la anterior.

## Advertencias

* Asegúrese de que las imágenes de entrada estén en el formato correcto y tengan el nombre adecuado según las instrucciones de cada archivo.

* Si encuentra problemas con las bibliotecas, asegúrese de que estén instaladas correctamente usando pip.
