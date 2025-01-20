import cv2
import math
import ultralytics
import numpy as np
import easyocr  # OCR para reconocimiento de placas
import time  # Para controlar el tiempo transcurrido

# Carga del modelo YOLOv8
model = ultralytics.YOLO("Other/yolov8l-oiv7.pt")

# Configuración de texto y color para las cajas y etiquetas
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.7
thickness = 2

# Clases de interés
clases_interes = ['Person', 'Motorcycle', 'Helmet']

# Cargar OCR con EasyOCR
ocr = easyocr.Reader(['en'])

# Carga del video
cap = cv2.VideoCapture('Resource/Videos/Video_Para_Programar.MOV')

def calcular_centro(x1, y1, x2, y2):
    """Calcula el centroide de una caja delimitadora."""
    return ((x1 + x2) // 2, (y1 + y2) // 2)

def reconocer_placa(imagen_placa):
    """Extrae texto de una imagen de placa usando OCR."""
    resultado_ocr = ocr.readtext(imagen_placa)
    if resultado_ocr:
        return resultado_ocr[0][1]  # Devuelve el texto de la primera detección
    return ""

# Procesar el video cuadro por cuadro
last_detected_time = None  # Tiempo en que se detectó la motocicleta y persona
placa_img = None  # Imagen de la placa
placa_texto = ""  # Texto de la placa

while cap.isOpened():
    ret, frame = cap.read()  
    if not ret:  
        break

    # Detección con YOLO en el cuadro actual
    results = model(frame)

    # Diccionario para almacenar objetos detectados
    detecciones = {
        'Person': [],
        'Motorcycle': [],
        'Helmet': []
    }

    # Procesar detecciones
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            class_name = r.names[class_id]
            confidence = math.ceil(box.conf[0] * 100)

            # Filtrar por clases de interés
            if class_name in clases_interes:
                centroide = calcular_centro(x1, y1, x2, y2)
                detecciones[class_name].append((x1, y1, x2, y2, centroide, confidence))

    # Asignar motocicletas a personas y cascos a personas
    asociaciones = []
    placas_detectadas = []  # Lista de placas extraídas

    for (px1, py1, px2, py2, p_centro, p_conf) in detecciones['Person']:
        moto_cercana = None
        casco_cercano = None
        min_dist_moto = float('inf')
        min_dist_casco = float('inf')

        # Buscar la motocicleta más cercana
        for (mx1, my1, mx2, my2, m_centro, m_conf) in detecciones['Motorcycle']:
            distancia = np.linalg.norm(np.array(p_centro) - np.array(m_centro))
            if distancia < min_dist_moto:
                min_dist_moto = distancia
                moto_cercana = (mx1, my1, mx2, my2, m_conf)

        # Buscar el casco más cercano
        for (hx1, hy1, hx2, hy2, h_centro, h_conf) in detecciones['Helmet']:
            distancia = np.linalg.norm(np.array(p_centro) - np.array(h_centro))
            if distancia < min_dist_casco:
                min_dist_casco = distancia
                casco_cercano = (hx1, hy1, hx2, hy2, h_conf)

        # Asociar persona con su moto y casco
        asociaciones.append((px1, py1, px2, py2, p_conf, moto_cercana, casco_cercano))

    # Dibujar detecciones y asociaciones
    for (px1, py1, px2, py2, p_conf, moto, casco) in asociaciones:
        # Dibujar persona
        cv2.rectangle(frame, (px1, py1), (px2, py2), (0, 255, 0), 2)
        cv2.putText(frame, f"Person {p_conf}%", (px1, py1 - 10), font, fontScale, (0, 255, 0), thickness)

        # Dibujar motocicleta y verificar si necesita escanear placa
        if moto:
            mx1, my1, mx2, my2, m_conf = moto
            cv2.rectangle(frame, (mx1, my1), (mx2, my2), (255, 0, 0), 2)
            cv2.putText(frame, f"Motorcycle {m_conf}%", (mx1, my1 - 10), font, fontScale, (255, 0, 0), thickness)

            # Si la persona NO tiene casco, preparar escaneo de placa
            if not casco:
                # Crear un subframe utilizando las coordenadas de la motocicleta
                placa_img = frame[my1:my2, mx1:mx2]  # Se usa la misma región para el subframe de la motocicleta

                if placa_img.size > 0:
                    # Si no se ha detectado la placa previamente o si han pasado 0.5 segundos
                    if last_detected_time is None or time.time() - last_detected_time >= 0.5:
                        placa_texto = reconocer_placa(placa_img)
                        placas_detectadas.append((mx1, my1, placa_texto))

                        # Mostrar el valor de la placa en la consola
                        print(f"Placa detectada: {placa_texto}")

                        # Actualizar el tiempo de detección
                        last_detected_time = time.time()

                    # Dibujar la placa detectada en el video
                    cv2.rectangle(frame, (mx1, my1), (mx2, my2), (0, 165, 255), 2)
                    cv2.putText(frame, f"Placa: {placa_texto}", (mx1, my1 - 10), font, fontScale, (0, 165, 255), thickness)

                    # Mostrar el subframe de la placa en una ventana separada
                    cv2.imshow("Subframe Placa", placa_img)

        # Dibujar casco si hay
        if casco:
            hx1, hy1, hx2, hy2, h_conf = casco
            cv2.rectangle(frame, (hx1, hy1), (hx2, hy2), (0, 0, 255), 2)
            cv2.putText(frame, f"Helmet {h_conf}%", (hx1, hy1 - 10), font, fontScale, (0, 0, 255), thickness)

    # Mostrar el cuadro procesado
    cv2.imshow('Video', frame)

    # Presiona 'q' para salir del bucle
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()