# DataBase/TblPersona.py

# Psudo-Base de Datos de personas
usuarios_db = {
    "ID811E": {"nombre": "Hugo Vargas", "telefono": "+593996907332", "correo": "dotafrozen1@gmail.com"},
    "AA5601": {"nombre": "Dayana Paladines", "telefono": "+593983045751", "correo": "dayana.paladines@espoch.edu.ec"},
    "HA0501": {"nombre": "Alex Vallejo", "telefono": "+593980551466", "correo": "alexvallejo325@gmail.com"},
    "AP5001": {"nombre": "Marco Angamarca", "telefono": "+5930999859689", "correo": "vangamarca4@gmail.com"},
    "GU0201": {"nombre": "Daniela Robalino", "telefono": "+593995676927", "correo": "catherin.robalino@espoch.edu.ec"},
}

# Función para obtener información de la persona por placa
def obtener_usuario_por_placa(placa):
    return usuarios_db.get(placa, None)