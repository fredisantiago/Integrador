import mysql.connector
import serial
def conectar():
    global miConexion
    # Establece la conexión a la base de datos
    miConexion = mysql.connector.connect(
        host='localhost',
        user='root',       # Tu nombre de usuario de MySQL
        password='',       # Tu contraseña de MySQL (si la tienes)
        database='rentabicis'   # El nombre de la base de datos que deseas conectar
    )
# Crea un cursor para ejecutar consultas
def insertar(nombreCompleto,curp,numCuenta,telefono,tipo,costo,horaPrestamo, serial):
    cur = miConexion.cursor()
    # Consulta de inserción
    consulta_insertar = ("INSERT INTO `usuarios`(`id_Usuario`, `nombreCompleto`, `curp`, `numCuenta`, "
                    "`numTelefonico`, `tipo`, `costo`, `horaPrestamo`, `horaEntrega`) "
                    "VALUES (NULL,%s, %s, %s, %s, %s, %s, %s,NULL)")
    valores_insertar = (nombreCompleto, curp, numCuenta, telefono,tipo,costo,horaPrestamo)
    cur.execute(consulta_insertar, valores_insertar)
    miConexion.commit()
    # Cierra el cursor y la conexión
    cur.close()
    miConexion.close()
def actualizar(horaEntrega,numCuenta):
    cur = miConexion.cursor()
    # Consulta de inserción
    consulta_actualizar = "UPDATE usuarios SET horaEntrega = %s WHERE numCuenta = %s"
    valores_actualizar = (horaEntrega, numCuenta)
    cur.execute(consulta_actualizar, valores_actualizar)
    miConexion.commit()
    cur.close()
    miConexion.close()
def buscar(numCuenta):
    cur = miConexion.cursor()
    consulta_datos = "SELECT horaPrestamo, horaEntrega, tipo FROM usuarios WHERE numCuenta = %s"
    valores_consulta = (numCuenta)
    cur.execute(consulta_datos, valores_consulta)
    resultado = cur.fetchone()
    if resultado:
        horaPrestamo = resultado[0]
        horaEntrega = resultado[1]
        tipo=resultado[2]
        HorasRentada=horaEntrega-horaPrestamo
        return (HorasRentada*tipo)
    else:
        print("Registro no encontrado.")

    miConexion.close()
    
















