import easyocr
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO  # Importar YOLOv8
import numpy as np

# Cargar el modelo YOLOv8
model = YOLO("Other/yolov8l-oiv7.pt")

# Definir las clases de interés y sus colores
clases_interes = {'Person': (255, 0, 0), 'Motorcycle': (0, 255, 0), 'Helmet': (0, 0, 255)}

# Cargar la imagen
image_path = 'Resource/Images/ImagenMoto1.jpg'
image = cv2.imread(image_path)
original_image = image.copy()

# Realizar la detección con YOLO
results_yolo = model(image)[0]

# Variable para almacenar el recorte de la motocicleta
motorcycle_crop = None

# Dibujar las detecciones de YOLO en la imagen
for detection in results_yolo.boxes.data:
    x1, y1, x2, y2, conf, class_id = detection.tolist()
    class_name = model.names[int(class_id)]
    
    if class_name in clases_interes:
        color = clases_interes[class_name]
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        cv2.putText(image, f'{class_name} {conf:.2f}', (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Guardar el recorte de la motocicleta con margen para mejorar OCR
        if class_name == 'Motorcycle':
            margin = 20  # Aumentar margen para mejorar precisión del OCR
            x1, y1, x2, y2 = max(0, int(x1 - margin)), max(0, int(y1 - margin)), min(original_image.shape[1], int(x2 + margin)), min(original_image.shape[0], int(y2 + margin))
            motorcycle_crop = original_image[y1:y2, x1:x2]

# Crear el lector EasyOCR con ajuste de GPU y aumento de contraste
reader = easyocr.Reader(['es'], gpu=True)

# Si se detectó una motocicleta, mejorar la imagen y escanear en esa región
concatenated_text = ""
if motorcycle_crop is not None:
    # Aumentar la resolución y hacer zoom
    scale_factor = 2.0  # Factor de escala para aumentar resolución
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

# Imprimir el texto concatenado
print(f'Texto concatenado sin espacios: {concatenated_text}')

# Mostrar la imagen con los resultados
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image)
plt.axis('off')
plt.show()

# Mostrar la imagen recortada de la motocicleta con OCR si existe
if motorcycle_crop is not None:
    motorcycle_crop = cv2.cvtColor(motorcycle_crop, cv2.COLOR_BGR2RGB)
    plt.figure()
    plt.imshow(motorcycle_crop)
    plt.axis('off')
    plt.show()
