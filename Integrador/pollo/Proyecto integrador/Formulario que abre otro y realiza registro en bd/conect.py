import mysql.connector


def conectar():
    global miConexion
    # Establece la conexión a la base de datos
    miConexion = mysql.connector.connect(
        host='localhost',
        user='root',       # Tu nombre de usuario de MySQL
        password='',       # Tu contraseña de MySQL (si la tienes)
        database='organigrama'   # El nombre de la base de datos que deseas conectar
    )
def insertar(numCuenta,nombre,ap,am,rfc,numTelefonico, tipo, costo):
    cur = miConexion.cursor()
    # Consulta de inserción
    consulta_insertar = ("INSERT INTO `usuarios`(`id_usuario`, `numCuenta`, `nombre`, `apellidoP`, `apellidoM`, `rfc`, `numTelefonico`, `tipo`, `costo`, `horaPrestamo`, `horaEntrega`, `total`)"
                        "VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,"",0)")
    valores_insertar = ()
    cur.execute(consulta_insertar, valores_insertar)
    miConexion.commit()
    # Cierra el cursor y la conexión
    cur.close()
    miConexion.close()
##Deberan hacer el metodo para realizar registro de saidaa  similar a la de insertar pero con el 
# update pero esto se debera hacer en php para el codigo qr