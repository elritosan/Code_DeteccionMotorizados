# Services/Notificaciones.py
import random
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from Utils.Procesamiento import validar_placa
from DataBase.TblPersona import obtener_usuario_por_placa, usuarios_db  # Importar la base de datos de usuarios
from DataBase.TblNotificacion import obtener_notificacion_por_indice, notificaciones_db  # Importar la base de datos de notificaciones

# Función para enviar correo
def enviar_correo(smtp_host, smtp_port, smtp_user, smtp_password, origen, destino, mensaje):
    try:
        msg = MIMEText(mensaje)
        msg['Subject'] = 'Notificación de Seguridad'
        msg['From'] = origen  # Origen de la notificación
        msg['To'] = destino   # Destino de la notificación

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Iniciar TLS para seguridad
            server.login(smtp_user, smtp_password)  # Autenticación con SMTP
            server.sendmail(msg['From'], msg['To'], msg.as_string())  # Enviar correo
        
        print(f"Correo enviado a {destino}")
    except Exception as e:
        print(f"Error al enviar correo: {e}")


# Función para enviar WhatsApp
def enviar_whatsapp(account_sid, auth_token, origen_telefono, destino, mensaje):
    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=mensaje,
            from_=f'whatsapp:{origen_telefono}',  # Número de WhatsApp de origen parametrizado
            to=f'whatsapp:{destino}'              # Número de WhatsApp de destino
        )
        print(f"WhatsApp enviado a {destino}")
    except Exception as e:
        print(f"Error al enviar WhatsApp: {e}")

# Función para seleccionar aleatoriamente y procesar notificaciones
def procesar_notificaciones(motorizados, smtp_host, smtp_port, smtp_user, smtp_password, origen_email, origen_telefono, account_sid, auth_token):
    for motorizado in motorizados:
        if motorizado.placa and validar_placa(motorizado.placa):
            if motorizado.personas != motorizado.cascos:
                if motorizado.placa in usuarios_db:
                    usuario = obtener_usuario_por_placa(motorizado.placa)
                    nombre = usuario['nombre']
                    telefono = usuario['telefono']
                    correo = usuario['correo']

                    # Seleccionar aleatoriamente una notificación
                    indice_aleatorio = random.choice(list(range(1, len(notificaciones_db) + 1)))
                    mensaje = obtener_notificacion_por_indice(indice_aleatorio)
                    mensaje = mensaje.format(nombre=nombre)

                    # Enviar notificaciones
                    enviar_correo(smtp_host, smtp_port, smtp_user, smtp_password, origen_email, correo, mensaje)
                    enviar_whatsapp(account_sid, auth_token, origen_telefono, telefono, mensaje)

                else:
                    print(f"No se encontró usuario para la placa {motorizado.placa}")
        else:
            print(f"Placa inválida: {motorizado.placa}")