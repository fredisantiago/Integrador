import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import cv2
import os
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

# ...

fondo_path = "ImagenesInterfaz/fondo2.jpg"
fecha_hoy = datetime.now().date()
parametros = {"curp"}  # Cambiado a llaves {} en lugar de corchetes [] para indicar un conjunto

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=2,
    border=2,
)
qr.add_data(parametros)
qr.make(fit=True)
qr_image = qr.make_image(fill_color="black", back_color="white")
qr_image_path = f"CodigosQRI/1_QR.png"
qr_image.save(qr_image_path)
# FIN DEL CODIGO QR

# Inicio de tomar la foto
# Capturar una foto utilizando OpenCV
messagebox.showinfo("Vale", "Sonríe para la foto")
cam = cv2.VideoCapture(0)
return_value, image = cam.read()
cv2.imwrite("FotosI/foto_invitado.jpg", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
cam.release()

# Crear una credencial con la foto, nombre, CURP y número de departamento
foto_path = "FotosI/foto_invitado.jpg"
nombre_residente = "Pedro"
curp_residente = "ncnowio23nw3ocno2cn"
num_departamento ="10"
credencial_path = f"FotosI/credencial_invitado_1.pdf"
logo_path = "ImagenesInterfaz/logo.png"

# Tamaño del marco
ancho_marco = 480
alto_marco = 250

# Crear una imagen de credencial
credencial = canvas.Canvas(credencial_path, pagesize=(ancho_marco, alto_marco))
credencial.drawImage(fondo_path, 0, 0, width=ancho_marco, height=alto_marco)

# Agregar imagen al ticket
foto = Image.open(foto_path)
foto = foto.resize((100, 100), Image.LANCZOS)
credencial.drawInlineImage(foto_path, 20, alto_marco - 120, width=100, height=100)

# Pegamos el código QR (reemplaza qr_image con tu variable)
qr_width, qr_height = qr_image.size
credencial.drawInlineImage(qr_image, ancho_marco - 300, alto_marco - 90, width=qr_width, height=qr_height)

# Pegamos el logo
logo = Image.open(logo_path)
logo = logo.resize((80, 110), Image.LANCZOS)
credencial.drawInlineImage(logo_path, 160, alto_marco - 190, width=80, height=110)

font_size = 16
font_path = "Helvetica"  # Cambia a la ruta de la fuente Arial en tu sistema

# Agregar texto a la credencial
credencial.setFont(font_path, font_size)
credencial.setFillColorRGB(0, 0, 0)  # Texto en negro
credencial.drawString(220, alto_marco - 40, "Martillazo *")
credencial.drawString(160, alto_marco - 65, f"Nombre: {nombre_residente}")
credencial.drawString(160, alto_marco - 85, f"CURP: {curp_residente}")
credencial.drawString(160, alto_marco - 105, f"Fecha: {fecha_hoy}")
fecha_hoy

# Guardar la credencial
credencial.save()

# Cerrar la ventana de captura si estaba abierta
cv2.destroyAllWindows()
