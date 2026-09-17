# TP Programación sobre Redes

## Sistema Cliente-Servidor con Python y SQLite

Este proyecto implementa un sistema cliente-servidor utilizando sockets TCP/IP en Python.

El servidor escucha conexiones en `localhost:5000`, recibe mensajes enviados por los clientes y los almacena en una base de datos SQLite.

## Funcionalidades

* Servidor TCP/IP en `localhost:5000`.
* Cliente capaz de enviar múltiples mensajes.
* Almacenamiento de mensajes en SQLite.
* Registro de:

  * ID
  * Contenido
  * Fecha de envío
  * IP del cliente
* Confirmación del servidor mediante timestamp.
* Manejo de errores de conexión y base de datos.
* Finalización del cliente mediante la palabra `"éxito"`.

## Archivos

* `servidor.py`: contiene la implementación del servidor.
* `cliente.py`: contiene la implementación del cliente.
* `mensajes.db`: base de datos SQLite utilizada para almacenar los mensajes.

## Cómo ejecutar

### 1. Iniciar el servidor

Abrir una terminal y ejecutar:

```bash
python servidor.py
```

El servidor quedará escuchando conexiones en `localhost:5000`.

### 2. Iniciar el cliente

Abrir una segunda terminal y ejecutar:

```bash
python cliente.py
```

### 3. Enviar mensajes

El cliente permite ingresar y enviar múltiples mensajes.

El servidor recibe cada mensaje, lo almacena en la base de datos y devuelve una confirmación con la fecha y hora de recepción.

Para finalizar la conexión se debe escribir:

```text
éxito
```

## Base de datos

La aplicación utiliza SQLite mediante el módulo `sqlite3` de Python.

La tabla `mensajes` almacena los siguientes datos:

* `id`: identificador único del mensaje.
* `contenido`: texto enviado por el cliente.
* `fecha_envio`: fecha y hora del mensaje.
* `ip_cliente`: dirección IP del cliente.

## Prueba realizada

Se realizaron pruebas locales ejecutando primero el servidor y luego el cliente en una segunda terminal.

Se verificó el envío de múltiples mensajes, la respuesta del servidor con el timestamp y el almacenamiento de los mensajes en la base de datos SQLite.

## Tecnologías utilizadas

* Python
* Sockets TCP/IP
* SQLite
* Módulo `sqlite3`
