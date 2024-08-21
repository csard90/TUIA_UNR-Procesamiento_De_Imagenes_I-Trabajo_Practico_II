import cv2
import numpy as np
from matplotlib import pyplot as plt

# Elegir entre las distintas listas de acuerdo a lo que se quiere ver, cambiar el nombre de la lista en el for
funciona_con = ['img02.png', 'img04.png', 'img05.png', 'img06.png','img09.png', 'img10.png']
no_funciona = ['img01.png', 'img03.png', 'img07.png', 'img08.png', 'img11.png', 'img12.png']
todas = ['img01.png', 'img02.png', 'img03.png', 'img04.png', 'img05.png', 'img06.png', 'img07.png', 'img08.png','img09.png', 'img10.png', 'img11.png', 'img12.png']

for imagen in funciona_con:
    # Cargar la imagen a colores
    img = cv2.imread(f'Imagenes/{imagen}', cv2.IMREAD_COLOR)
        
    # Convertir imagen a escala de grises
    img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Umbralado 
    img_umbralada = cv2.threshold(img_gris, 121, 255, cv2.THRESH_BINARY)[1]

    # Componentes conectadas
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_umbralada)    

    # Filtramos elementos con áreas muy pequeñas y muy chicas

    # Esta copia del labels (que la vamos modificando) y la siguiente fueron hechas para no sobrescribir
    # variables y poder ir controlando el flujo del código a medida que aparecían errores
    labels_copia = labels.copy()

    # Recorremos cada componente conectado sin incluir el fondo
    for i in range(num_labels):

        # Los que tengan un area superior e inferior a determinados umbrales
        if stats[i, -1] < 26 or stats[i, -1] > 98:
            
            # Los eliminamos
            labels_copia[labels_copia == i] = 0
    
    # En las imágenes resultantes además de las letras quedan otros elementos 

    # De los elementos que nos quedaron del filtrado por area queremos filtrar ahora por la relación entre
    # ancho y alto, pero en stats tenemos informacion demas. Por lo que volveremos a buscar sobre el resultado
    # anterior los componentes conectados y luego a evaluar con los stats la relación entre ancho y alto.
    
    casi_letras = cv2.threshold(labels_copia.astype(np.uint8), 0, 255, cv2.THRESH_BINARY)[1]       
    num_labels_2, labels_2, stats_2, centroids_2 = cv2.connectedComponentsWithStats(casi_letras)
    
    labels_copia_2 = labels_2.copy()
    # Recorremos todo menos el fondo
    for i in range(num_labels_2):
        # Eliminamos los elementos cuya relación ancho/alto no esté dentro del intervalo especificado
        if stats_2[i, 3]/stats_2[i, 2] < 1.5 or stats_2[i, 3]/stats_2[i, 2] > 4:
            labels_copia_2[labels_copia_2 == i] = 0

    # En mas de un caso aun quedan componentes conectados que no son letras pero si estan dentro de los
    # intervalos de area y relación ancho/alto establecidos. Para solucionar esto aun queda 
    # un paso mas que seria evaluar la distancia euclidea de los elementos. 

    # Al igual que en el paso anterior en las variables que contienen los centroides hay informacion demas
    # ya que solo eliminamos de los labels los elementos que no nos servian por lo que volvemos a buscar
    # componentes conectados para poder trabajar con la informacion completa actualizada

    casi_letras_2 = cv2.threshold(labels_copia_2.astype(np.uint8), 0, 255, cv2.THRESH_BINARY)[1]
    num_labels_3, labels_3, stats_3, centroids_3 = cv2.connectedComponentsWithStats(casi_letras_2)

    labels_copia_3 = labels_3.copy()
    # Recorremos todos los elementos
    for i in range(num_labels_3):
        # Inicializamos un contador        
        contador=0
        # Comparamos el elemento i con todo el resto de los elementos        
        for j in range(num_labels_3):
            # Calculamos las distancias euclídeas de todos con todos
            distancia_euclidea = np.sqrt(np.sum((centroids_3[i] - centroids_3[j]) ** 2))
            # Si la distancia está dentro de determinado umbral
            if distancia_euclidea > 3 and distancia_euclidea < 17:
                # Esos dos elementos están cerca
                contador+=1
        # Si el contador es 0 no hay ningún elemento cerca (no es una letra)
        if contador==0: 
            # Lo borramos
            labels_copia_3[labels_copia_3 == i] = 0
    
    # Volvemos a actualizar los componentes conectados que quedaron
    casi_letras_3 = cv2.threshold(labels_copia_3.astype(np.uint8), 0, 255, cv2.THRESH_BINARY)[1]
    num_labels_4, labels_4, stats_4, centroids_4 = cv2.connectedComponentsWithStats(casi_letras_3)

    # Copia de la imagen donde se mostrarán los resultados
    resultado_final = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Dibujamos los rectángulos en los caracteres
    for i in range(num_labels_4):
        resultado_final = cv2.rectangle(resultado_final, (stats_4[i, cv2.CC_STAT_LEFT], stats_4[i, cv2.CC_STAT_TOP]), 
                      (stats_4[i, cv2.CC_STAT_LEFT]+stats_4[i, cv2.CC_STAT_WIDTH] , 
                       stats_4[i, cv2.CC_STAT_TOP]+stats_4[i, cv2.CC_STAT_HEIGHT]), (0, 0, 255), 1)
    
    # Calculo de donde deberia ir el rectangulo de la patente
    # El if es para evitar, en caso que el algoritmo no haya funcionado bien y no quede ningun componente
    # conectado, excepciones por buscar el minimo en un array vacio. Si hay al menos un elemento más que
    # el fondo se realizan los calculos
    if len(stats_4) > 1:
        # En x el valor más a la izquierda
        izquierda = stats_4[1:, 0].min()    
        # En y el valor más arriba
        arriba = stats_4[1:, 1].min()    
        # En x el valor más a la derecha
        derecha = (stats_4[1:, 0] + stats_4[1:, 2]).max()
        # En y el valor más abajo
        abajo = (stats_4[1:, 1] + stats_4[1:, 3]).max()
        
        # Dibujamos el rectangulo de la patente
        # Los números de arriba se calcularon teniendo en cuenta los caracteres, pero la patente entera esta
        # un poco más lejos en cada una de las direcciones por eso los alejamos un poco.        
        resultado_final = cv2.rectangle(resultado_final, (int(izquierda-izquierda*0.03), int(arriba-arriba*0.03)), (int(derecha+derecha*0.03), int(abajo+abajo*0.03)), (255, 0, 0), 1) 
    
    # Mostrar resultado final
    plt.figure(), plt.imshow(resultado_final), plt.show()
    