# DataBase/TblNotificacion.py

# Psudo-Base de Datos de notificaciones con índices numéricos
notificaciones_db = {
    1: "¡Recordatorio! Por favor, recuerda usar tu casco de seguridad.",
    2: "¡Advertencia! La cantidad de personas en la moto es mayor que la cantidad de cascos.",
    # Puedes agregar más notificaciones con índices numéricos
}

# Función para obtener una notificación por su índice
def obtener_notificacion_por_indice(indice):
    return notificaciones_db.get(indice, None)
