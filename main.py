# main.py
import cv2
import matplotlib.pyplot as plt
from Services.Deteccion import detectar_motorizados
from Services.Reconocimiento_placas import reconocer_placa

def main():
    image_path = 'Resource/Images/ImagenMoto1.jpg'
    motorizados, original_image = detectar_motorizados(image_path)
    motorizados = reconocer_placa(original_image, motorizados)
    
    for motorizado in motorizados:
        motorizado.mostrar_info()
    
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()