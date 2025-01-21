import easyocr
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO  # Importar YOLOv8
import numpy as np
from datetime import datetime
from sklearn.neighbors import NearestNeighbors

# Cargar el modelo YOLOv8
model = YOLO("Other/yolov8l-oiv7.pt")

# Definir las clases de interés y sus colores
clases_interes = {'Person': (255, 0, 0), 'Motorcycle': (0, 255, 0), 'Helmet': (0, 0, 255)}

# Función para calcular el centroide de un cuadro delimitador (bounding box)
def calcular_centroid(x1, y1, x2, y2):
    return ((x1 + x2) / 2, (y1 + y2) / 2)

# Clase para almacenar la información de un motorizado
class ClassMotorizado:
    def __init__(self, id_motorizado, placa, fecha_hora):
        self.id_motorizado = id_motorizado
        self.placa = placa
        self.fecha_hora = fecha_hora
        self.personas = 0
        self.cascos = 0
        self.motorcycle_bbox = None
        self.centroid_motorcycle = None
        self.detected_objects = []

    def agregar_objeto(self, objeto, centroid):
        self.detected_objects.append((objeto, centroid))
        if objeto == 'Person':
            self.personas += 1
        elif objeto == 'Helmet':
            self.cascos += 1

    def asociar_motorcycle(self, bbox, centroid):
        self.motorcycle_bbox = bbox
        self.centroid_motorcycle = centroid

    def mostrar_info(self):
        print(f"ID: {self.id_motorizado}, Placa: {self.placa}, Fecha y Hora: {self.fecha_hora}")
        print(f"Personas en la moto: {self.personas}")
        print(f"Cascos detectados: {self.cascos}")
        print(f"Bounding box de la moto: {self.motorcycle_bbox}")
        print(f"Objetos detectados: {self.detected_objects}")


# Cargar la imagen
image_path = 'Resource/Images/ImagenMoto1.jpg'
image = cv2.imread(image_path)
original_image = image.copy()

# Realizar la detección con YOLO
results_yolo = model(image)[0]

# Almacenar motorizados detectados
motorizados = []
id_motorizado = 0

# Obtener la fecha y hora de la detección
fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Dibujar las detecciones de YOLO en la imagen
for detection in results_yolo.boxes.data:
    x1, y1, x2, y2, conf, class_id = detection.tolist()
    class_name = model.names[int(class_id)]
    
    if class_name in clases_interes:
        color = clases_interes[class_name]
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        cv2.putText(image, f'{class_name} {conf:.2f}', (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        centroid = calcular_centroid(x1, y1, x2, y2)
        print(f"Centroide de {class_name}: {centroid}")

        # Si es una motocicleta, crear un nuevo motorizado
        if class_name == 'Motorcycle':
            id_motorizado += 1
            motorizado = ClassMotorizado(id_motorizado, placa='', fecha_hora=fecha_hora)
            motorizado.asociar_motorcycle((x1, y1, x2, y2), centroid)
            motorizados.append(motorizado)

        # Si es una persona o casco, asociarlo a un motorizado cercano
        if class_name == 'Person' or class_name == 'Helmet':
            # Agrupar por proximidad usando kNN
            if motorizados:
                centroides_motorizados = [m.centroid_motorcycle for m in motorizados if m.centroid_motorcycle is not None]
                centroides_objetos = [centroid for class_name_ in ['Person', 'Helmet']]
                
                if centroides_motorizados:
                    # Crear el modelo kNN con 1 vecino (uno más cercano)
                    knn = NearestNeighbors(n_neighbors=1)
                    knn.fit(centroides_motorizados)
                    distances, indices = knn.kneighbors([centroid])  # Buscar el más cercano
                    print(f"Distancia de kNN: {distances}, Indices: {indices}")
                    
                    # Asignar la persona/casco al motorizado más cercano
                    if distances[0][0] < 250:  # Ajusta este umbral según sea necesario
                        motorizados[indices[0][0]].agregar_objeto(class_name, centroid)

# Crear el lector EasyOCR con ajuste de GPU y aumento de contraste
reader = easyocr.Reader(['es'], gpu=True)

# Extraer la placa de la motocicleta si es posible
concatenated_text = ""
for motorizado in motorizados:
    if motorizado.motorcycle_bbox is not None:
        x1, y1, x2, y2 = motorizado.motorcycle_bbox
        motorcycle_crop = original_image[int(y1):int(y2), int(x1):int(x2)]
        
        # Aumentar la resolución y hacer zoom
        scale_factor = 2.0
        motorcycle_crop = cv2.resize(motorcycle_crop, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        # Convertir a escala de grises y mejorar contraste
        gray = cv2.cvtColor(motorcycle_crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        results_ocr = reader.readtext(gray, detail=1, contrast_ths=0.7, adjust_contrast=0.5)
        for (bbox, text, prob) in results_ocr:
            concatenated_text += text.strip().replace(" ", "")
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            cv2.rectangle(motorcycle_crop, top_left, bottom_right, (0, 255, 255), 2)
            cv2.putText(motorcycle_crop, text, (top_left[0], top_left[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        motorizado.placa = concatenated_text

# Mostrar la información de los motorizados
for motorizado in motorizados:
    motorizado.mostrar_info()

# Mostrar la imagen con los resultados
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image)
plt.axis('off')
plt.show()

# Mostrar las imágenes de las motocicletas con OCR si existe
for motorizado in motorizados:
    if motorizado.motorcycle_bbox is not None:
        motorcycle_crop = cv2.cvtColor(motorcycle_crop, cv2.COLOR_BGR2RGB)
        plt.figure()
        plt.imshow(motorcycle_crop)
        plt.axis('off')
        plt.show()