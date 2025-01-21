# DataBase/TblPersona.py

# Psudo-Base de Datos de personas
usuarios_db = {
    "ID811E": {"nombre": "Hugo Vargas", "telefono": "+593996907332", "correo": "dotafrozen1@gmail.com"},
    "XYZ456": {"nombre": "María López", "telefono": "+593998888888", "correo": "maria.lopez@email.com"},
    # Agregar más usuarios según sea necesario
}

# Función para obtener información de la persona por placa
def obtener_usuario_por_placa(placa):
    return usuarios_db.get(placa, None)