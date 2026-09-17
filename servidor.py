import socket
import sqlite3
from datetime import datetime


# ============================================================
# CONFIGURACIÓN DEL SERVIDOR
# ============================================================

HOST = "127.0.0.1"
PORT = 5000
DB_NAME = "mensajes.db"


# ============================================================
# INICIALIZACIÓN DE LA BASE DE DATOS
# ============================================================

def inicializar_db():
    """
    Crea la base de datos SQLite y la tabla de mensajes
    si todavía no existen.
    """
    try:
        conexion = sqlite3.connect(DB_NAME)

        cursor = conexion.cursor()

        # Creamos la tabla donde se almacenarán los mensajes.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)

        conexion.commit()
        conexion.close()

        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as error:
        print(f"Error al acceder a la base de datos: {error}")
        raise


# ============================================================
# CONFIGURACIÓN DEL SOCKET TCP/IP
# ============================================================

def inicializar_socket():
    """
    Crea y configura el socket TCP/IP del servidor.
    """
    try:
        # AF_INET indica que utilizaremos IPv4.
        # SOCK_STREAM indica que utilizaremos TCP.
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Permite reutilizar el puerto cuando se reinicia el servidor.
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Asociamos el socket a localhost y al puerto 5000.
        servidor.bind((HOST, PORT))

        # El servidor queda preparado para recibir conexiones.
        servidor.listen(5)

        print(f"Servidor escuchando en {HOST}:{PORT}")

        return servidor

    except OSError as error:
        print(f"Error al iniciar el servidor. ¿El puerto {PORT} está ocupado?")
        print(f"Detalle del error: {error}")
        return None


# ============================================================
# GUARDAR MENSAJE EN LA BASE DE DATOS
# ============================================================

def guardar_mensaje(contenido, fecha_envio, ip_cliente):
    """
    Guarda un mensaje recibido en la base de datos SQLite.
    """
    try:
        conexion = sqlite3.connect(DB_NAME)

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """, (contenido, fecha_envio, ip_cliente))

        conexion.commit()
        conexion.close()

        print("Mensaje guardado correctamente en la base de datos.")

        return True

    except sqlite3.Error as error:
        print(f"Error al guardar el mensaje en la DB: {error}")
        return False


# ============================================================
# ACEPTAR CONEXIONES Y RECIBIR MENSAJES
# ============================================================

def atender_cliente(conexion_cliente, direccion_cliente):
    """
    Recibe mensajes de un cliente, los guarda en la DB
    y devuelve una confirmación.
    """

    print(f"Cliente conectado: {direccion_cliente}")

    try:
        while True:

            # Recibimos hasta 1024 bytes desde el cliente.
            datos = conexion_cliente.recv(1024)

            # Si no recibimos datos, el cliente cerró la conexión.
            if not datos:
                break

            # Convertimos los bytes recibidos a texto.
            mensaje = datos.decode("utf-8").strip()

            if not mensaje:
                continue

            # Obtenemos la fecha y hora actual del servidor.
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"Mensaje recibido: {mensaje}")

            # Guardamos el mensaje en la base de datos.
            guardado = guardar_mensaje(
                mensaje,
                timestamp,
                direccion_cliente[0]
            )

            # Si se pudo guardar, respondemos al cliente.
            if guardado:
                respuesta = f"Mensaje recibido: {timestamp}"
            else:
                respuesta = "Error: no se pudo guardar el mensaje."

            # Enviamos la respuesta al cliente.
            conexion_cliente.sendall(respuesta.encode("utf-8"))

    except ConnectionResetError:
        print("El cliente cerró la conexión inesperadamente.")

    except Exception as error:
        print(f"Error al atender al cliente: {error}")

    finally:
        # Cerramos la conexión con el cliente.
        conexion_cliente.close()
        print(f"Cliente desconectado: {direccion_cliente}")


# ============================================================
# EJECUCIÓN PRINCIPAL DEL SERVIDOR
# ============================================================

def iniciar_servidor():
    """
    Inicializa la base de datos y el socket,
    y comienza a aceptar conexiones.
    """

    # Primero inicializamos la base de datos.
    inicializar_db()

    # Después inicializamos el socket.
    servidor = inicializar_socket()

    # Si el socket no pudo crearse, terminamos el programa.
    if servidor is None:
        return

    try:
        while True:

            # Esperamos una nueva conexión de un cliente.
            conexion_cliente, direccion_cliente = servidor.accept()

            # Atendemos al cliente.
            atender_cliente(conexion_cliente, direccion_cliente)

    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")

    except Exception as error:
        print(f"Error en el servidor: {error}")

    finally:
        # Cerramos el socket del servidor.
        servidor.close()
        print("Socket del servidor cerrado.")


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    iniciar_servidor()