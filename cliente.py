import socket


# ============================================================
# CONFIGURACIÓN DEL CLIENTE
# ============================================================

HOST = "127.0.0.1"
PORT = 5000


# ============================================================
# CONECTAR CON EL SERVIDOR
# ============================================================

def conectar_servidor():
    """
    Crea un socket TCP/IP y se conecta al servidor.
    """

    try:
        # AF_INET utiliza IPv4.
        # SOCK_STREAM utiliza el protocolo TCP.
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Nos conectamos al servidor en localhost:5000.
        cliente.connect((HOST, PORT))

        print("Conectado correctamente al servidor.")
        print("Escribí tus mensajes.")
        print("Para finalizar escribí: éxito")
        print("-" * 50)

        return cliente

    except ConnectionRefusedError:
        print("No se pudo conectar con el servidor.")
        print("Verificá que servidor.py esté ejecutándose.")

        return None

    except Exception as error:
        print(f"Error al conectar con el servidor: {error}")

        return None


# ============================================================
# ENVIAR MENSAJES AL SERVIDOR
# ============================================================

def enviar_mensajes(cliente):
    """
    Permite al usuario enviar múltiples mensajes
    hasta escribir 'éxito'.
    """

    try:
        while True:

            # Solicitamos un mensaje al usuario.
            mensaje = input("Mensaje: ")

            # La palabra 'éxito' finaliza la comunicación.
            if mensaje.lower() == "éxito":
                print("Finalizando conexión...")
                break

            # Evitamos enviar mensajes vacíos.
            if not mensaje.strip():
                print("El mensaje no puede estar vacío.")
                continue

            # Enviamos el mensaje al servidor.
            cliente.sendall(mensaje.encode("utf-8"))

            # Esperamos la respuesta del servidor.
            respuesta = cliente.recv(1024)

            # Mostramos la confirmación recibida.
            print(f"Servidor: {respuesta.decode('utf-8')}")

    except ConnectionResetError:
        print("La conexión con el servidor se perdió.")

    except Exception as error:
        print(f"Error durante la comunicación: {error}")

    finally:
        # Cerramos la conexión.
        cliente.close()
        print("Conexión cerrada.")


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================

def main():
    """
    Función principal del cliente.
    """

    cliente = conectar_servidor()

    if cliente is not None:
        enviar_mensajes(cliente)


# Ejecutamos el programa principal.
if __name__ == "__main__":
    main()