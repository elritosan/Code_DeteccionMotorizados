# config.py
import cv2
from ultralytics import YOLO

# Cargar el modelo YOLOv8
MODEL_PATH = "Other/yolov8l-oiv7.pt"
model = YOLO(MODEL_PATH)

# Definir las clases de interés y sus colores
CLASES_INTERES = {'Person': (255, 0, 0), 'Motorcycle': (0, 255, 0), 'Helmet': (0, 0, 255)}
