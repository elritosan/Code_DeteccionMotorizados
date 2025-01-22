# DataBase/TblNotificacion.py

# Pseudo-Base de Datos de notificaciones con índices numéricos
notificaciones_db = {
    1: "¡Recordatorio! Por favor, recuerda usar tu casco de seguridad.",
    2: "¡Advertencia! La cantidad de personas en la moto es mayor que la cantidad de cascos.",
    3: "¡Seguridad primero! Asegúrate de que tu casco esté bien abrochado antes de iniciar el viaje.",
    4: "¡Cuidado! Un casco mal ajustado reduce su efectividad en caso de accidente.",
    5: "¡Importante! Usar casco puede salvar tu vida. No olvides colocártelo siempre.",
    6: "¡Atención! Verifica que tu casco no tenga daños visibles antes de usarlo.",
    7: "¡Normativa! Es obligatorio el uso del casco para todos los ocupantes del vehículo.",
    8: "¡Consejo! Los cascos certificados ofrecen mejor protección. Usa siempre uno homologado.",
    9: "¡Revisión! Cambia tu casco si ha sufrido un impacto fuerte, aunque no parezca dañado.",
    10: "¡Alerta! Conducir sin casco aumenta el riesgo de lesiones graves en caso de accidente.",
    11: "¡No lo olvides! La visera del casco protege tus ojos del polvo y los insectos.",
    12: "¡Seguridad vial! Siempre usa casco, sin importar la distancia que vayas a recorrer.",
    13: "¡Información útil! El uso del casco reduce en un 70% el riesgo de lesiones fatales.",
    14: "¡Obligatorio! El casco debe cubrir completamente la cabeza y ajustarse correctamente.",
    15: "¡Precaución! Conducir sin casco puede acarrear multas y sanciones.",
}

# Función para obtener una notificación por su índice
def obtener_notificacion_por_indice(indice):
    return notificaciones_db.get(indice, None)