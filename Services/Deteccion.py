# Services/Deteccion.py
import cv2
import numpy as np
from datetime import datetime
from config import model, CLASES_INTERES
from Utils.Procesamiento import calcular_centroid
from Models.Motorizado import ClassMotorizado
from sklearn.neighbors import NearestNeighbors

def detectar_motorizados(image_path):
    image = cv2.imread(image_path)
    original_image = image.copy()
    results_yolo = model(image)[0]
    motorizados = []
    id_motorizado = 0
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for detection in results_yolo.boxes.data:
        x1, y1, x2, y2, conf, class_id = detection.tolist()
        class_name = model.names[int(class_id)]
        
        if class_name in CLASES_INTERES:
            color = CLASES_INTERES[class_name]
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            centroid = calcular_centroid(x1, y1, x2, y2)
            print(f"Centroide de {class_name}: {centroid}")
            
            if class_name == 'Motorcycle':
                id_motorizado += 1
                motorizado = ClassMotorizado(id_motorizado, placa='', fecha_hora=fecha_hora)
                motorizado.asociar_motorcycle((x1, y1, x2, y2), centroid)
                motorizados.append(motorizado)
            
            if class_name in ['Person', 'Helmet'] and motorizados:
                centroides_motorizados = [m.centroid_motorcycle for m in motorizados if m.centroid_motorcycle]
                if centroides_motorizados:
                    knn = NearestNeighbors(n_neighbors=1)
                    knn.fit(centroides_motorizados)
                    distances, indices = knn.kneighbors([centroid])
                    print(f"Distancia de kNN: {distances}, Indices: {indices}")
                    if distances[0][0] < 250:
                        motorizados[indices[0][0]].agregar_objeto(class_name, centroid)
    
    return motorizados, original_image