import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import time
import datetime
### Librerias para mandar mensajes

from email.message import EmailMessage
import ssl
import smtplib

### Importar serial 
import serial
from Bicicleta import Bicicl
import Conexion as con

import tkinter as tk
from tkinter import messagebox
########################
###################
##############
ser = serial.Serial('COM3', 9600)

##################
########################
def recibirInformacionSerial():
    # Abre el puerto serial (ajusta el puerto y velocidad según tu configuración)
    while True:
        linea = ser.readline().decode('utf-8').strip()
        if linea != "":
            con.conectar()
            horaEntrega = datetime.datetime.now()
            con.actualizar(horaEntrega,linea)
            totalPagar=con.buscar(linea)

            ventanaPago = tk.Toplevel(root)
            ventanaPago.title("Bicicleta entregada")
            label = tk.Label(ventanaPago, text="Tu pago sera de : "+str() )
            label.pack()
def enviardatos(ventana,bici):
    global entry_nombre, entry_curp, entry_num_cuenta, entry_telefono,tipo
    nombre = entry_nombre.get()
    curp = entry_curp.get()
    num_cuenta = entry_num_cuenta.get()
    telefono = entry_telefono.get()
    tip=bice.costo
    cost=bice.costo
    con.conectar();
    hora_actual = datetime.datetime.now()
    con.insertar(nombreCompleto=nombre,curp=curp,numCuenta=
                 num_cuenta,telefono=telefono,tipo=tip,costo=cost,horaPrestamo=hora_actual,serial=ser)
    # Aquí pes donde se mandan los datos a arduino, unicamente se debera enviar el dato mas significativo ya que recordando
    #tiene un limite de almacenamiento la tarjeta RFID
    ser.write(num_cuenta.encode())
    mensaje = f"Datos guardados:\nNombre: {nombre}\nCURP: {curp}\nNúmero de Cuenta: {num_cuenta}\nTeléfono: {telefono}"
    messagebox.showinfo("Datos Guardados", mensaje)
    cerrarVentana(ventana)

def pedirBici(bicla):
    global entry_nombre, entry_curp, entry_num_cuenta, entry_telefono,nueva_ventana
    nueva_ventana = tk.Toplevel(root)
    nueva_ventana.title("Registro de usuario")
    label_nombre = tk.Label(nueva_ventana, text="Nombre Completo:")
    entry_nombre = tk.Entry(nueva_ventana)
    label_curp = tk.Label(nueva_ventana, text="CURP:")
    entry_curp = tk.Entry(nueva_ventana)
    label_num_cuenta = tk.Label(nueva_ventana, text="Número de Cuenta:")
    entry_num_cuenta = tk.Entry(nueva_ventana)
    label_telefono = tk.Label(nueva_ventana, text="Número Telefónico:")
    entry_telefono = tk.Entry(nueva_ventana)
    btn_guardar = tk.Button(nueva_ventana, text="Guardar", command=lambda:enviardatos(nueva_ventana,bicla))
    label_nombre.pack()
    entry_nombre.pack()
    label_curp.pack()
    entry_curp.pack()
    label_num_cuenta.pack()
    entry_num_cuenta.pack()
    label_telefono.pack()
    entry_telefono.pack()
    btn_guardar.pack()
    # Deshabilitar la ventana principal
    root.attributes("-disabled", True)
    # Llamar a la función para reactivar la ventana principal cuando se cierre la secundaria
    nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: cerrarVentana(nueva_ventana))

def cerrarVentana(ventana):
    # Cerrar la ventana secundaria y reactivar la ventana principal
    ventana.destroy()
    root.attributes("-disabled", False)



def Reporte():
     ###Configura variables de mensajes
    mensaje=" "
    for bici in bicicletas:
        mensaje += f"de tipo bici.tipo fueron:"+ str(totalderentas)+"n"
    mensaje=mensaje+"Con un total de ingresos de: "+ str(totaldeingresos)
    passw ="yyzhcynnkltmrljc"
    envia="ingpollo1525@gmail.com"
    recibe="lui1525angel@gmail.com"
    asunto="Conteo y resumen de pet"
##Crear instancia de EmailMessage
    correo=EmailMessage()
    correo["From"]= envia
    correo["To"]=recibe
    correo["Subject"]=asunto
    correo.set_content(mensaje)  
    
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
        smtp.login(envia,passw)
        smtp.sendmail(envia,recibe,correo.as_string())
###Interface

## Configurar puerto
##ser = serial.Serial('COM3', 9600) 
# Crear una ventana para mostrar el video
root = tk.Tk()
root.title("Renta de bicicletas")

# Configurar la imagen de fondo
bg_image = PhotoImage(file="Fondo.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Ocupa todo el espacio de la ventana
#####
########
###Variables
todoterreno=Bicicl("todoterreno",10, 0,50, "todoterreno.png")
pista=Bicicl("pista",10,0,60,"pista.png")
cruiser=Bicicl("cruiser",10,0,90,"cruice.png")
competicion=Bicicl("competicion",10,1,100,"competicion.png")
bicicletas=[todoterreno,pista,cruiser,competicion]
totalderentas=0
totaldeingresos=0
# Cargar imágenes para las etiquetas

exit_image = PhotoImage(file="Exit.png")

# Crear un frame
frame = tk.Frame(root, bg="white")
frame.configure(background='#4EB6FF')
frame.pack(side="top", fill="x")
# Organizar elementos en dos columnas
col = 0
contadores_labels = {}

for bice in bicicletas:
    btn = tk.Button(frame, image=bice.imagen, command=lambda b=bice: pedirBici(b))
    btn.grid(row=0, column=col, padx=10, pady=10)
    lblcontador = tk.Label(frame, text=f"Costo por hora: ${bice.costo}")
    lblcontador.grid(row=1, column=col)
    lblestado = tk.Label(frame, text=f"Unidades disponibles: {bice.stock}")
    lblestado.grid(row=2, column=col)
    col += 1
    if col == 3:
        btn = tk.Button(frame, text="Enviar resumen", command=lambda: Reporte(), foreground="#ff0000",
                  activeforeground="#FFA500", width = 50)
        btn.grid(row=3, column=2)

# Configurar el tamaño de la ventana según el contenido
root.update_idletasks()
frame_width = root.winfo_width()
frame_height = root.winfo_height()

# Añadir un margen para una mejor apariencia
extra_width = 20
extra_height = 20

# Establecer tamaño de la ventana
root.geometry(f"{frame_width + extra_width}x{frame_height + extra_height}")

# Iniciar el bucle de eventos
root.mainloop()

