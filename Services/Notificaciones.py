# Services/Notificaciones.py
import random
import smtplib
from email.mime.text import MIMEText
from Utils.Procesamiento import validar_placa
from DataBase.TblPersona import obtener_usuario_por_placa, usuarios_db
from DataBase.TblNotificacion import obtener_notificacion_por_indice, notificaciones_db

# Configuración del servidor SMTP de Hotmail
SMTP_HOST = "smtp.office365.com"
SMTP_PORT = 587

# Función para enviar correo desde Hotmail
def enviar_correo_hotmail(usuario, contraseña, destinatario, mensaje):
    try:
        # Crear el mensaje
        msg = MIMEText(mensaje)
        msg['Subject'] = 'Notificación de Seguridad'
        msg['From'] = usuario
        msg['To'] = destinatario

        # Conectar al servidor SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # Activar seguridad TLS
            server.login(usuario, contraseña)  # Autenticación
            server.sendmail(usuario, destinatario, msg.as_string())  # Enviar correo
        
        print(f"✅ Correo enviado a {destinatario}")
    
    except smtplib.SMTPAuthenticationError:
        print("❌ Error: No se pudo autenticar con Hotmail. Verifica tu usuario y contraseña.")
    except smtplib.SMTPException as e:
        print(f"❌ Error al enviar correo: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

# Función para procesar las notificaciones
def procesar_notificaciones(motorizados, usuario, contraseña):
    for motorizado in motorizados:
        if motorizado.placa and validar_placa(motorizado.placa):
            if motorizado.personas != motorizado.cascos:
                if motorizado.placa in usuarios_db:
                    usuario_data = obtener_usuario_por_placa(motorizado.placa)
                    nombre = usuario_data['nombre']
                    correo = usuario_data['correo']

                    # Seleccionar notificación aleatoria
                    indice_aleatorio = random.choice(list(range(1, len(notificaciones_db) + 1)))
                    mensaje = obtener_notificacion_por_indice(indice_aleatorio)
                    mensaje = mensaje.format(nombre=nombre)

                    # Enviar correo
                    enviar_correo_hotmail(usuario, contraseña, correo, mensaje)

                else:
                    print(f"⚠ No se encontró usuario para la placa {motorizado.placa}")
        else:
            print(f"⚠ Placa inválida: {motorizado.placa}")