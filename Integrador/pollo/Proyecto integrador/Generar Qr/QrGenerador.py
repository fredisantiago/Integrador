import qrcode
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Genera el enlace con los parámetros para el registro
base_url = "https://tu-servidor.com/registrar.php?"#normalmente va a ser localhost seguido del nombre de la carpeta despues el nomnbre del arcivo php
parametros = {"curp": "GOFL009933HMCLNS01"}  # datos que se van a enviar al archivo php para 
#registrar la salida, bastaria con enviar, la curp o rfc
enlace_registro = base_url + "&".join([f"{key}={value}" for key, value in parametros.items()])

# Genera el código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(enlace_registro)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("registro_qr.png")##Nombre y ubicacion del qr generado

# Configura el correo electrónico  se hizo en practicas anteriores
email_from = "tucorreo@gmail.com"
email_to = "destinatario@gmail.com"
subject = "Código QR para registro"
body = "Adjunto encontrarás el código QR para el registro de salida."

# Configura el mensaje
message = MIMEMultipart()
message.attach(MIMEText(body, "plain"))

# Adjunta el código QR al correo electrónico
attachment = open("registro_qr.png", "rb")
message.attach(MIMEText(attachment.read(), "base64"))
attachment.close()

# Configura el servidor de correo
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "tucorreo@gmail.com"
smtp_password = "tucontraseña"

# Inicia sesión en el servidor de correo y envía el correo
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)
server.sendmail(email_from, email_to, message.as_string())
server.quit()
