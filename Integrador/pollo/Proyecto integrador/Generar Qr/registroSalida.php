<?php
// Configuración de la conexión a la base de datos
$servername = "tu_servidor";
$username = "tu_usuario";
$password = "tu_contraseña";
$dbname = "tu_base_de_datos";

// Parámetros recibidos desde el código QR
$curp = $_GET['curp'];

// Conecta a la base de datos
$conn = new mysqli($servername, $username, $password, $dbname);

// Verifica la conexión
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

// Inserta los datos en la base de datos (esto es un ejemplo, puedes adaptarlo según tu estructura de base de datos)
$sql = "INSERT INTO tu_tabla (nombre, edad) VALUES ('$curp')";//Cambiar por la instruccion update

if ($conn->query($sql) === TRUE) {
    echo "Registro exitoso";
} else {
    echo "Error al registrar: " . $conn->error;
}

// Cierra la conexión
$conn->close();
?>
