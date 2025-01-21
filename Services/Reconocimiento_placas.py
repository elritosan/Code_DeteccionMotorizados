# Services/Reconocimiento_placas.py
import easyocr
import cv2

def reconocer_placa(image, motorizados):
    reader = easyocr.Reader(['es'], gpu=True)
    for motorizado in motorizados:
        if motorizado.motorcycle_bbox:
            x1, y1, x2, y2 = motorizado.motorcycle_bbox
            motorcycle_crop = image[int(y1):int(y2), int(x1):int(x2)]
            motorcycle_crop = cv2.resize(motorcycle_crop, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(motorcycle_crop, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            results_ocr = reader.readtext(gray, detail=1, contrast_ths=0.7, adjust_contrast=0.5)
            concatenated_text = "".join(text.strip().replace(" ", "") for _, text, _ in results_ocr)
            motorizado.placa = concatenated_text
    return motorizados