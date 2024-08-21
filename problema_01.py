import cv2
import numpy as np
from matplotlib import pyplot as plt

# Cargamos la imagen a colores
img = cv2.imread('Imagenes/monedas.jpg', cv2.IMREAD_COLOR)

# Convertimos imagen a escala de grises
img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicammos el filtro pasabajos para suavizado:
img_blur = cv2.GaussianBlur(img_gris, ksize=(5, 5), sigmaX=1.5)   

# Aplicamos Canny para segmentar
img_canny = cv2.Canny(img_blur, threshold1=20, threshold2=150) 
        
# Dilatammos para engrosar un poco los bordes y después poder rellenarlos
elemento_estructural_1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (40, 40))
img_dilatada = cv2.dilate(img_canny, elemento_estructural_1, iterations=1)   

# Encontramos los contornos
contours, _ = cv2.findContours(img_dilatada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Creamos una imagen en blanco para dibujar los contornos y rellenar
imagen_rellena = np.zeros_like(img_dilatada)

# Dibujamos y rellenamos los contornos en la imagen en blanco
imagen_rellena = cv2.drawContours(imagen_rellena, contours, -1, 255, thickness=cv2.FILLED) 

# Erosión para dar más forma a los círculos
elemento_estructural_2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20)) 
img_erosionada = cv2.erode(imagen_rellena, elemento_estructural_2, iterations=3) 

# Buscamos componentes conectadas
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_erosionada) 

# Copia de la imagen sobre la que vamos a dibujar rectángulos
img_clasificada = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Contadores de objetos
cantidad_monedas = 0
cantidad_dados = 0
monedas_1= 0
monedas_50= 0
monedas_10= 0

# Vamos analizando elemento a elemento recorriendo desde el primer elemento, que no es el fondo, en adelante
for i in range(1, num_labels):
    # Generamos una matriz con todos 0 salvo donde está el elemento que se está analizando
    obj = (labels == i).astype(np.uint8)
    
    # Obtenemos el contorno del elemento
    contour, _ = cv2.findContours(obj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculamos el factor de forma del elemento
    area = cv2.contourArea(contour[0])
    perimetro = cv2.arcLength(contour[0], True)
    ff = area / perimetro**2

    # Si el factor de forma es mayor que un umbral establecido experimentalmente, es una moneda
    if ff > 0.065:            
        cantidad_monedas+=1           
        
        if 53000 > stats[i, cv2.CC_STAT_AREA] > 48000:
            # Dibujamos rectángulo sobre la imagen
            img_clasificada = cv2.rectangle(img_clasificada, (stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP]), (stats[i, cv2.CC_STAT_LEFT]+stats[i, cv2.CC_STAT_WIDTH] , stats[i, cv2.CC_STAT_TOP]+stats[i, cv2.CC_STAT_HEIGHT]), (255, 0, 0), 4)        
            monedas_10+=1
        elif stats[i, cv2.CC_STAT_AREA] > 72000 and stats[i, cv2.CC_STAT_AREA] < 77000:
            # Dibujamos rectángulo sobre la imagen
            img_clasificada = cv2.rectangle(img_clasificada, (stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP]), (stats[i, cv2.CC_STAT_LEFT]+stats[i, cv2.CC_STAT_WIDTH] , stats[i, cv2.CC_STAT_TOP]+stats[i, cv2.CC_STAT_HEIGHT]), (0, 255, 0), 4)        
            monedas_1+=1
        else:            
            # Dibujamos rectángulo sobre la imagen
            img_clasificada = cv2.rectangle(img_clasificada, (stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP]), (stats[i, cv2.CC_STAT_LEFT]+stats[i, cv2.CC_STAT_WIDTH] , stats[i, cv2.CC_STAT_TOP]+stats[i, cv2.CC_STAT_HEIGHT]), (255, 255, 255), 4)        
            monedas_50+=1

    # Si no, es un dado
    else:
        cantidad_dados+=1

        # Dibujamos un rectángulo sobre la imagen
        img_clasificada = cv2.rectangle(img_clasificada, (stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP]), (stats[i, cv2.CC_STAT_LEFT]+stats[i, cv2.CC_STAT_WIDTH] , stats[i, cv2.CC_STAT_TOP]+stats[i, cv2.CC_STAT_HEIGHT]), (0, 0, 255), 4)

        # Cropping de la imagen de canny de los bounding box de los dados.
        dado_canny= img_canny[ stats[i, cv2.CC_STAT_TOP] : stats[i, cv2.CC_STAT_TOP]+stats[i, cv2.CC_STAT_HEIGHT], stats[i, cv2.CC_STAT_LEFT]:stats[i, cv2.CC_STAT_LEFT]+stats[i, cv2.CC_STAT_WIDTH ]]
    
        # Dilatamos para ensanchar los bordes un poco para cerrar los contornos de los círculos
        elemento_estructural_3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
        dado_dilatado = cv2.dilate(dado_canny, elemento_estructural_3, iterations=1) 

        # Rellenamos los contornos para rellenar los circulitos y dilatamos la imagen
        contours, _ = cv2.findContours(dado_dilatado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        imagen_rellena = np.zeros_like(dado_dilatado)
        dado_dilatado = cv2.drawContours(dado_dilatado, contours, -1, 255, thickness=cv2.FILLED)     
        
        # Contamos los números de los dados:
        # La idea es que como los círculos van a tener áreas similares, podes establecer un umbral de modo experimental
        num_labels_dados, labels_dados, stats_dados, centroids_dados = cv2.connectedComponentsWithStats(dado_dilatado)        
        contador_numeros=0
        for j in range(1, num_labels_dados):
            if stats_dados[j, cv2.CC_STAT_AREA] > 2600 and stats_dados[j, cv2.CC_STAT_AREA] < 2800:
                contador_numeros += 1 
        
        # Escribimos el número en la imagen
        img_clasificada = cv2.putText(img_clasificada, str(contador_numeros), (stats[i, cv2.CC_STAT_LEFT]+20, stats[i, cv2.CC_STAT_TOP]+150), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10)  

# Escribimos sobre la imagen la cantidad de monedas y dados detectados
img_clasificada = cv2.putText(img_clasificada, f'Cantidad de monedas: {cantidad_monedas}', (140,2100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
img_clasificada = cv2.putText(img_clasificada, f'Cantidad de 10 cvos: {monedas_10}', (140,2180), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 8)
img_clasificada = cv2.putText(img_clasificada, f'Cantidad de 50 cvos: {monedas_50}', (140,2260), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 8)
img_clasificada = cv2.putText(img_clasificada, f'Cantidad de 1 peso: {monedas_1}', (140,2340), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 8)
img_clasificada = cv2.putText(img_clasificada, f'Cantidad de dados: {cantidad_dados}', (140,2420), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)

# Resultado final
plt.figure()
plt.imshow(img_clasificada, cmap='gray')
plt.show()