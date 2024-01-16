import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import cv2
import os
import qrcode

#Inicio de Validaciones
def validate_nombre(P):
   return P.replace(" ", "").isalpha() or P.isspace() or P == ""

def validate_telefono(P):
    return P.isdigit() or P == ""

def validate_curp(P):
    return P.isalnum() or P == ""

def validate_edad(P):
    return P.isdigit() or P == ""

def validate_dep(P):
    return P.isdigit() or P == ""

#Fin de Validaciones
#Funcion para el boton de residente
def mostrar_residente(ventana):
    #Inicio de guardar Residente
    # Botón de guardar
    def guardar_residente():
        # Obtener los datos ingresados por el usuario
        nombre = NR.get()
        telefono = TR.get()
        curp = CR.get()
        sexo = SR.get()
        edad = ER.get()
        numero_departamento = combo_departamentos.get()
        print(telefono)
        
        # Validar que no haya campos vacíos
        if not (nombre and telefono and curp and edad and sexo and numero_departamento):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="interfoon",
            port='3307'
        )
        cursor = conexion.cursor()

            # Obtener el último id_Residentes insertado
        cursor.execute("SELECT MAX(id_Residentes) FROM residentes")
        ultimo_id = cursor.fetchone()[0]

        # Calcular el nuevo id_Residentes
        nuevo_id = 1 if ultimo_id is None else ultimo_id + 1

        # Actualizar el estatus del departamento en la tabla de departamentos
        cursor.execute("UPDATE departamento SET estatus = 1 WHERE No_departamento = %s", (numero_departamento,))

        # Insertar el residente en la tabla de residentes
        insert_query = "INSERT INTO residentes (id_Residentes, Nombre_residentes, telefono, edad, curp, sexo, no_de_fk) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        residente_data = (nuevo_id, nombre, telefono, edad, curp, sexo, numero_departamento)
        cursor.execute(insert_query, residente_data)

        # Confirmar la transacción y cerrar la conexión
        conexion.commit()
        conexion.close()

        print("Residente guardado con éxito")
        #Creamos el codigo QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
            )
        qr.add_data(curp)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image_path = f"CodigosQR/{nombre}_QR.png"
        qr_image.save(qr_image_path)
        #FIN DEL CODIGO QR
        
        #Inicio de tomar la foto
        # Capturar una foto utilizando OpenCV
        messagebox.showinfo("Vale", "Sonrie para la foto")
        cam = cv2.VideoCapture(0)
        return_value, image = cam.read()
        cv2.imwrite("Fotos/foto_residente.jpg", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        cam.release()

        # Crear una credencial con la foto, nombre, CURP y número de departamento
        foto_path = "Fotos/foto_residente.jpg"
        nombre_residente = NR.get()
        curp_residente = CR.get()
        num_departamento = combo_departamentos.get()
        credencial_path = f"Fotos/credencial_residente_{nuevo_id}.png"

        # Crear una imagen de credencial
        credencial = Image.new('RGB', (400, 200), color='white')
        foto = Image.open(foto_path)
        foto = foto.resize((100, 100), Image.LANCZOS)
        credencial.paste(foto, (10, 10))
        
        #Pegamos el codigo qr 
        qr_width, qr_height = qr_image.size
        credencial.paste(qr_image, (260, 60, 260 + qr_width, 60 + qr_height)) 
        draw = ImageDraw.Draw(credencial)
        font = ImageFont.load_default()
        
         # Utilizar la fuente Arial con tamaño 14
        font_size = 14
        font_path = "arial.ttf"  # Cambia a la ruta de la fuente Arial en tu sistema
        font = ImageFont.truetype(font_path, size=font_size)

        # Agregar texto a la credencial
        draw.text((120, 5), f"HOTEL MARTILLAZO *", fill='black', font=font )
        draw.text((120, 30), f"Nombre: {nombre_residente}", fill='black', font=font)
        draw.text((120, 50), f"CURP: {curp_residente}", fill='black', font=font)
        draw.text((120, 70), f"Departamento: {num_departamento}", fill='black', font=font)

        # Guardar la credencial
        credencial.save(credencial_path)

        # Cerrar la ventana de captura si estaba abierta
        cv2.destroyAllWindows()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Residente guardado con éxito. Credencial generada.")
        #Fin de tomar la Foto
    
    #Fin de guardar Residente
    #ventana de nuevo 
    def nuevo_residente():
        # Limpiamos las cajas de texto y ComboBox
        NR.delete(0, tk.END)
        TR.delete(0, tk.END)
        ER.delete(0, tk.END)
        CR.delete(0, tk.END)
        SR.set("") 
        combo_departamentos.set("")  
        
    #Ventana de Residente
    ventana.destroy()
    VResidente=tk.Tk()
    VResidente.configure(bg="cyan3")
    VResidente.geometry("300x450")
    
    #Boton de regresar
    imagen_atras = Image.open("ImagenesInterfaz/atras.jpg")
    imagen = ImageTk.PhotoImage(imagen_atras)
    boton_regresar = tk.Button(
        VResidente, image=imagen, compound=tk.LEFT,
        command=lambda: mostrar_principal(VResidente), height=35, width=35
    )
    boton_regresar.pack(pady=5,side='left',anchor='n')
    
    #Inicio Cajas de texto para llenar los datos:
    #Nombre del residente
    Nresidente = tk.Label(VResidente, text="Nombre Completo", font=("Arial", 10, "bold"), fg="Black")
    Nresidente.pack(pady=5)
    vcmd_nombre = (VResidente.register(validate_nombre), '%P')
    NR = tk.Entry(VResidente, validate="key", validatecommand=vcmd_nombre)
    NR.pack(pady=4)
    
    #Telefono del residente
    Nresidente = tk.Label(VResidente, text="Telefono", font=("Arial", 10, "bold"), fg="Black")
    Nresidente.pack(pady=5)
    vcmd_telefono = (VResidente.register(validate_telefono), '%P')
    TR = tk.Entry(VResidente, validate="key", validatecommand=vcmd_telefono)
    TR.pack(pady=4)
    
    #Edad del residente
    Nresidente = tk.Label(VResidente, text="Edad", font=("Arial", 10, "bold"), fg="Black")
    Nresidente.pack(pady=5)
    vcmd_edad=(VResidente.register(validate_edad),'%P')
    ER = tk.Entry(VResidente,validate="key",validatecommand=vcmd_edad)
    ER.pack(pady=4)
    
    #CURP del residente
    Nresidente = tk.Label(VResidente, text="CURP", font=("Arial", 10, "bold"), fg="Black")
    Nresidente.pack(pady=5)
    vcmd_curp=(VResidente.register(validate_curp),'%P')
    CR = tk.Entry(VResidente,validate="key",validatecommand=vcmd_curp)
    CR.pack(pady=4)
    
    #SEXO del residente
    Nresidente = tk.Label(VResidente, text="SEXO", font=("Arial", 10, "bold"), fg="Black")
    Nresidente.pack(pady=5)
    opciones_sexos = ["Masculino", "Femenino", "Salchicha","Otro","prefiero no decirlo", "Jonathan ALberto"]
    SR = ttk.Combobox(VResidente, values=opciones_sexos,state="readonly")
    SR.pack(pady=4)
    #Numero de Departamentos
    Nresidente = tk.Label(VResidente, text="Numero de Departamento", font=("Arial", 10, "bold"), fg="Black")
    Nresidente.pack(pady=5)
 
    # Conectar a la base de datos MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="interfoon",
        port= '3307'
    )
    cursor = conexion.cursor()

    # Obtener los datos de los departamentos disponibles
    cursor.execute("SELECT No_departamento, Num_ext, Num_piso FROM departamento WHERE estatus = 0")
    departamentos_disponibles = cursor.fetchall()
    
    # Crear una lista con los números de los departamentos disponibles
    opciones_departamentos = [departamento[0] for departamento in departamentos_disponibles]
    
    # Crear el Combobox con los departamentos disponibles
    combo_departamentos = ttk.Combobox(VResidente, values=opciones_departamentos, state="readonly")
    combo_departamentos.pack(pady=4)
    # Función para actualizar el exterior y piso al seleccionar un departamento
    def actualizar_exterior_piso(event):
        numero_departamento = combo_departamentos.get()
        for departamento in departamentos_disponibles:
            if str(departamento[0]) == numero_departamento:
                exterior, piso = departamento[1], departamento[2]
                exterior_label.config(text=f"Exterior: {exterior}")
                piso_label.config(text=f"Piso: {piso}")

                # Agregar instrucciones de impresión para depuración
                print(f"Número de Departamento: {numero_departamento}")
                print(f"Exterior: {exterior}")
                print(f"Piso: {piso}")

                
    # Etiquetas para mostrar el exterior y piso
    exterior_label = tk.Label(VResidente, text="Exterior: ")
    exterior_label.pack(pady=5)

    piso_label = tk.Label(VResidente, text="Piso: ")
    piso_label.pack(pady=5)

    # Asociar la función de actualización al evento de selección del Combobox
    combo_departamentos.bind("<<ComboboxSelected>>", actualizar_exterior_piso)
    
    # Cerrar la conexión después de utilizar los datos
    conexion.close()
        #Fin de numero de departamento
        #Fin de la caja del formulario
        #   Boton
    btn_G_residentes = tk.Button(text="Guardar", command=guardar_residente, height=1, width=8)
    btn_G_residentes.pack(pady=5, side='left', anchor='s')
    
    #NUEVO
    btn_N_residentes = tk.Button(text="NUEVO", command=nuevo_residente, height=1, width=8)
    btn_N_residentes.pack(pady=5, side='right', anchor='s')
    
    print("Residente")
    imagen_atras.close()
    VResidente.mainloop()
#Funcion para el boton de Invitado
def mostrar_invitado():
    #Inicio de interfaz Invitado
    
    #Fin de interfaz residente
    
    print("Invitado")
#Funcion para la ventana Principal
def mostrar_principal(ventana_actual=None):
    #Verificamos que ventana esta activa
    if ventana_actual:
        ventana_actual.destroy()
    # Ventana
    ventana = tk.Tk()
    ventana.geometry("600x400")
    ventana.title("Integrador")

    # Ruta de la imagen de fondo
    img0 = "ImagenesInterfaz/fondo.jpg"
    imagen_fondo_pil = Image.open(img0)
    imgfondo = ImageTk.PhotoImage(imagen_fondo_pil)

    # Ponemos la imagen de fondo en la ventana
    fondo = tk.Label(ventana, image=imgfondo)
    fondo.place(relwidth=1, relheight=1) # Ocupa todo el espacio de la Interfaz

    #Titulo
    titulo = tk.Label(ventana, text="Hotel Martillazo *", font=("Arial", 20, "bold italic"), fg="Black")
    titulo.pack(pady=5)

    # Imagen de dai
    ruta_imagen = "ImagenesInterfaz/dani.jpg"
    imagen_pil = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen_pil)
    dani = tk.Label(ventana, image=imagen)
    dani.image = imagen
    dani.pack(pady=5)

    # Boton de Ingresar Residente
    boton_residente = tk.Button(ventana, text="Residente", command=lambda:mostrar_residente(ventana), height=2, width=20)
    boton_residente.pack(pady=10)

    # Boton de Ingresar Invitado
    boton_invitado = tk.Button(ventana, text="Invitado", command=lambda:mostrar_invitado(ventana), height=2, width=20)
    boton_invitado.pack(pady=10)

    # Iniciar el bucle principal de la interfaz gráfica
    ventana.mainloop()
    
    
#Corremos la ventana
mostrar_principal()
