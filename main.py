import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Services.Deteccion import detectar_motorizados
from Services.Reconocimiento_placas import reconocer_placa
from Services.Notificaciones import procesar_notificaciones
from DataBase.TblMotorizadosPostgreSQL import ClassTblMotorizadosPostgreSQL  # Importar la clase de inserción

# Configuración de credenciales para Hotmail
HOTMAIL_USER = "alex.vallejom@espoch.edu.ec"
HOTMAIL_PASSWORD = "password123"

class MotoDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección de Motorizados y Placas")
        self.root.state("zoomed")  # Maximizar ventana automáticamente
        self.root.configure(bg="#f0f0f0")  # Fondo de la ventana principal

        # Imagen de fondo
        self.bg_image = Image.open("Resource/Images/Background_DM.jpg")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Marco principal con color de fondo y bordes
        self.frame = tk.Frame(root, bg="#ffffff", relief="ridge", bd=5)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=1050, height=550)

        # Título en la parte superior con color y nueva fuente
        self.lbl_titulo = tk.Label(self.frame, text="Detección de Motorizados", font=("Helvetica", 18, "bold"), bg="#0073e6", fg="white")
        self.lbl_titulo.pack(fill="x", pady=5)

        # Contenedor principal con alineación horizontal
        self.content_frame = tk.Frame(self.frame, bg="#ffffff")
        self.content_frame.pack(expand=True, pady=10)

        # Área de imágenes alineadas en la misma fila con mayor tamaño
        self.lbl_imagen_original = tk.Label(self.content_frame, bg="#ffffff")
        self.lbl_imagen_original.grid(row=0, column=0, padx=10, pady=5)
        
        self.lbl_imagen_procesada = tk.Label(self.content_frame, bg="#ffffff")
        self.lbl_imagen_procesada.grid(row=0, column=1, padx=10, pady=5)

        # Área de información detectada con fuente más moderna
        self.lbl_info = tk.Label(self.content_frame, text="", font=("Helvetica", 16), bg="#ffffff", fg="#333333", justify="left", anchor="w")
        self.lbl_info.grid(row=0, column=2, padx=10, pady=5)

        # Contenedor para los botones con color de fondo
        self.btn_frame = tk.Frame(self.frame, bg="#ffffff")
        self.btn_frame.pack(side=tk.BOTTOM, pady=5)

        # Botón para cargar imagen con nuevo estilo
        self.btn_cargar = tk.Button(self.btn_frame, text="Cargar Imagen", bg="#0073e6", fg="white", font=("Helvetica", 12), command=self.cargar_imagen)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        # Botón para procesar imagen con nuevo estilo
        self.btn_procesar = tk.Button(self.btn_frame, text="Procesar Imagen", bg="#0073e6", fg="white", font=("Helvetica", 12), command=self.procesar_imagen, state=tk.DISABLED)
        self.btn_procesar.pack(side=tk.RIGHT, padx=5)

        # Botón para volver al inicio (oculto inicialmente)
        self.btn_reset = tk.Button(self.btn_frame, text="Volver al Inicio", bg="#0073e6", fg="white", font=("Helvetica", 12), command=self.reset_interface)

        # Variable para almacenar la ruta de la imagen cargada
        self.image_path = None

    def cargar_imagen(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg *.png *.jpeg")])
        
        if self.image_path:
            # Cargar y mostrar la imagen original en la interfaz
            img_original = Image.open(self.image_path)
            img_original.thumbnail((400, 350), Image.Resampling.LANCZOS)
            img_original = ImageTk.PhotoImage(img_original)

            self.lbl_imagen_original.config(image=img_original)
            self.lbl_imagen_original.image = img_original

            # Asegurar que el botón de procesar se mantenga visible
            self.btn_procesar.pack(side=tk.RIGHT, padx=5)
            self.btn_procesar.config(state=tk.NORMAL)

    def procesar_imagen(self):
        if not self.image_path:
            return

        # Ocultar el botón de cargar imagen y mostrar el de volver al inicio
        self.btn_cargar.pack_forget()
        self.btn_reset.pack(side=tk.LEFT, padx=5)

        # Detectar motorizados y reconocer placas
        motorizados, original_image, image_detecciones = detectar_motorizados(self.image_path)
        motorizados = reconocer_placa(original_image, motorizados)

        # Crear instancia de la clase para realizar la inserción en la base de datos
        motorizados_db = ClassTblMotorizadosPostgreSQL()
        info_text = ""

        # Procesar cada motorizado y mostrar la información
        for motorizado in motorizados:
            info_text += f"Placa: {motorizado.placa}\nPersonas: {motorizado.personas}\nCascos: {motorizado.cascos}\n\n"
            motorizado.mostrar_info()

            # Insertar el motorizado en la base de datos
            motorizados_db.insert_into_motorizados(
                motorizado.placa,  # Placa
                motorizado.personas,  # Número de personas
                motorizado.cascos  # Número de cascos
            )

        # Actualizar la etiqueta con la información detectada
        self.lbl_info.config(text=info_text)

        # Convertir imágenes a RGB para matplotlib
        image_detecciones_rgb = cv2.cvtColor(image_detecciones, cv2.COLOR_BGR2RGB)
        
        # Redimensionar correctamente la imagen procesada sin deformarla
        img_result = Image.fromarray(image_detecciones_rgb)
        img_result.thumbnail((400, 350), Image.Resampling.LANCZOS)
        img_result = ImageTk.PhotoImage(img_result)

        self.lbl_imagen_procesada.config(image=img_result)
        self.lbl_imagen_procesada.image = img_result

    def reset_interface(self):
        self.lbl_imagen_original.config(image="")
        self.lbl_imagen_procesada.config(image="")
        self.lbl_info.config(text="")
        self.btn_procesar.config(state=tk.DISABLED)
        self.image_path = None
        self.btn_reset.pack_forget()
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

# Crear la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MotoDetectorApp(root)
    root.mainloop()
