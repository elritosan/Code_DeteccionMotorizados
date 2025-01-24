import re

# Utils/Procesamiento.py
def calcular_centroid(x1, y1, x2, y2):
    return ((x1 + x2) / 2, (y1 + y2) / 2)

# Función para validar que la placa tenga 6 caracteres alfanuméricos
def validar_placa(placa):
    return bool(re.match(r'^[A-Z0-9]{6}$', placa))