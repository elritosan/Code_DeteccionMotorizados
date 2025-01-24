# main.py

import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from Services.Deteccion import detectar_motorizados
from Services.Reconocimiento_placas import reconocer_placa
from Services.Notificaciones import procesar_notificaciones
from DataBase.TblMotorizadosPostgreSQL import ClassTblMotorizadosPostgreSQL  # Importar la clase de inserción

# Configuración de credenciales para Hotmail
HOTMAIL_USER = "hugos.vargas@espoch.edu.ec"
HOTMAIL_PASSWORD = "MiPassword123"

class MotoDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección de Motorizados y Placas")
        self.root.geometry("800x900")

        # Botón para cargar imagen
        self.btn_cargar = tk.Button(root, text="Cargar Imagen", command=self.cargar_imagen)
        self.btn_cargar.pack(pady=10)

        # Área de imagen
        self.lbl_imagen = tk.Label(root)
        self.lbl_imagen.pack()

        # Botón para procesar imagen
        self.btn_procesar = tk.Button(root, text="Procesar Imagen", command=self.procesar_imagen, state=tk.DISABLED)
        self.btn_procesar.pack(pady=10)

        # Variable para almacenar la ruta de la imagen cargada
        self.image_path = None

    def cargar_imagen(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg *.png *.jpeg")])
        
        if self.image_path:
            # Cargar y mostrar la imagen en la interfaz
            img = Image.open(self.image_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)

            self.lbl_imagen.config(image=img)
            self.lbl_imagen.image = img

            # Habilitar el botón de procesamiento
            self.btn_procesar.config(state=tk.NORMAL)

    def procesar_imagen(self):
        if not self.image_path:
            return

        # Detectar motorizados y reconocer placas
        motorizados, original_image, image_detecciones = detectar_motorizados(self.image_path)
        motorizados = reconocer_placa(original_image, motorizados)

        # Crear instancia de la clase para realizar la inserción en la base de datos
        motorizados_db = ClassTblMotorizadosPostgreSQL()

        # Procesar cada motorizado y mostrar la información
        for motorizado in motorizados:
            motorizado.mostrar_info()

            # Insertar el motorizado en la base de datos
            motorizados_db.insert_into_motorizados(
                motorizado.placa,  # Placa
                motorizado.personas,  # Número de personas
                motorizado.cascos  # Número de cascos
            )

        # Enviar notificaciones
        procesar_notificaciones(motorizados, HOTMAIL_USER, HOTMAIL_PASSWORD)

        # Convertir imágenes a RGB para matplotlib
        original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        image_detecciones_rgb = cv2.cvtColor(image_detecciones, cv2.COLOR_BGR2RGB)

        # Mostrar imágenes en una nueva ventana con Matplotlib
        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.imshow(original_image_rgb)
        plt.title("Imagen Original")
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(image_detecciones_rgb)
        plt.title("Imagen con Detecciones")
        plt.axis('off')

        plt.show()

# Crear la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MotoDetectorApp(root)
    root.mainloop()