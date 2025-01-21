# Models/Motorizado.py
from datetime import datetime

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