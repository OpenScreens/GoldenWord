# subsistemas
Información sobre cada subsistema/objeto/microservicio en la infraestructura. Como identificar a cada uno, su proposito, y ejemplos.
## client: programa/codigo que se ejecuta en el dispositivo del usuario. La mayoría son controlados por terceros (Ejemplo Discord, Telegram, algun React frontend)
## msg 3ero: Servidor HTTP controlado por terceros que conecta cliente con otros backends, ejemplo (servidor de Discord API server o Telegram API server)
## msg: Servidor HTTP, único proposito es intermediar entre client con biz, hay uno por cada client (ejemplo Disco o Telegrama)
## biz: Servidor HTTP, contiene logica de negocio. (ejemplo Ping Pong, Poker Pal)


# Conexiones
Información de protocolos de red a usar para cada subsistema.
## HTTP server<-> HTTP server
La conexión entre servidores HTTP es a través de requests HTTP.
## Cliente <-> HTTP Server
La conexión típicamente es a través de WebSockets, algunas versiones de prueba usaran Polling o Long-Polling


## client->msg
El cliente envía mensajes normalmente con un request HTTP, la respuesta no debería contener información.
## msg->client
Al no exponer un puerto el cliente, el cliente deberá iniciar la conexión, sea mediante Polling, Long-Polling o Websockets.

## msg<-->biz
Los mensajes serán enviados a través de requests HTTP. La reply de un mensaje HTTP no puede contener infromación, solo un status code.
Las "respuestas" deberan consistir de otro mensaje HTTP.

## msg 3ero<-->biz
No siempre se puede controlar la arquitectura, deberá ser lo más parecida posible a msg<-->biz


## client<->biz
No

## Encripción
La encripción HTTPS se realiza con un microservicio adicional cuyo único o principal rol sea encriptar la conexión y redirigirla al subsistema, no sería practico que cada subsistema encripte y desencripte. El encriptador a utilizar es el ALB de aws.
Solo se encriptará la conexión entre cliente y msg.  

## Polling
Si un servidor msg, tuviera una conexión directa con un msg3, puede enviar los mensajes de biz tal como los recibe sin almacenarlos.
Si un servidor msg se conecta directamente con el cliente, deberá almacenar los mensajes de biz hasta que sean pedidos por client, en ese momento los destruirá.


# API
Información sobre el contenido de los mensajes a transmitir. El formato de estos, su autentificación
## client->msg3
Segun especifique la documentación de 3ero, la implementación puede ser mediante HTTP o utilizando una librería OFICIAL del proveedor. De no haber tal librería, no usar librerías no oficiales.

##msg->biz
{"message":"Hola",
"chatid":"237821732", //Típicamente un id de usuario al ser mensajes directos.
"frontend":"react"
}

##biz->msg
{"response":"Como estás?",
"chatid":"237821732"
}
## client->msg
en caso de transmitir un mensaje a msg propio y no de terceros, utilizar el mismo formato. que de msg a biz.
## msg->client
mismo formato que biz->msg, posibilidad de usar un array de mensajes.

## encoding type
Puede usarse multipart form data o x-www-urlencoded, asegurandosé que ambas partes puedan decodificar el mensaje. Asegurarse que no sean posibles ataques con escaping.
Es preferible no usar librerías de terceros, sino librerías incluidas en los lenguajes

python (envío): http.client o urllib> requests
python (recepción): http.server> flask
python (parseo): urllib.parse >flask.request.form

