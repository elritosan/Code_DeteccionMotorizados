import cv2
import matplotlib.pyplot as plt
from Services.Deteccion import detectar_motorizados
from Services.Reconocimiento_placas import reconocer_placa
from Services.Notificaciones import procesar_notificaciones

# Configuración de credenciales y datos para notificaciones
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "tu_correo@example.com"
SMTP_PASSWORD = "tu_contraseña"
ORIGEN_EMAIL = "notificaciones@ejemplo.com"
ORIGEN_TELEFONO = "+14155238886"  # Número de Twilio
ACCOUNT_SID = "tu_account_sid"
AUTH_TOKEN = "tu_auth_token"

def main():
    image_path = 'Resource/Images/ImagenMoto1.jpg'
    motorizados, original_image, image_detecciones = detectar_motorizados(image_path)
    motorizados = reconocer_placa(original_image, motorizados)
    
    for motorizado in motorizados:
        motorizado.mostrar_info()
    
    # Procesar notificaciones
    procesar_notificaciones(
        motorizados, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, 
        ORIGEN_EMAIL, ORIGEN_TELEFONO, ACCOUNT_SID, AUTH_TOKEN
    )
    
    # Convertir ambas imágenes a RGB para mostrarlas con matplotlib
    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    image_detecciones_rgb = cv2.cvtColor(image_detecciones, cv2.COLOR_BGR2RGB)
    
    # Mostrar las imágenes en subgráficas
    plt.figure(figsize=(10, 5))

    # Mostrar la imagen original
    plt.subplot(1, 2, 1)
    plt.imshow(original_image_rgb)
    plt.title("Imagen Original")
    plt.axis('off')

    # Mostrar la imagen con las detecciones
    plt.subplot(1, 2, 2)
    plt.imshow(image_detecciones_rgb)
    plt.title("Imagen con Detecciones")
    plt.axis('off')

    plt.show()

if __name__ == "__main__":
    main()