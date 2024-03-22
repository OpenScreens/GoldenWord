==subsistemas
client: programa/codigo que se ejecuta en el dispositivo del usuario. La mayoría son controlados por terceros (Ejemplo Discord, Telegram, algun React frontend)
msg 3ero: Servidor HTTP controlado por terceros que conecta cliente con otros backends, ejemplo (servidor de Discord API server o Telegram API server) 
msg: Servidor HTTP, único proposito es intermediar entre client con biz, hay uno por cada client (ejemplo Disco o Telegrama)
biz: Servidor HTTP, contiene logica de negocio. (ejemplo Ping Pong, Poker Pal)


==Conexiones
===HTTP server<-> HTTP server
La conexión entre servidores HTTP es a través de requests HTTP.
===Cliente <-> HTTP Server
La conexión típicamente es a través de WebSockets, algunas versiones de prueba usaran Polling o Long-Polling


===client->msg
El cliente envía mensajes normalmente con un request HTTP, la respuesta no debería contener información.
===msg->client
Al no exponer un puerto el cliente, el cliente deberá iniciar la conexión, sea mediante Polling, Long-Polling o Websockets.

===msg<-->biz
Los mensajes serán enviados a través de requests HTTP. La reply de un mensaje HTTP no puede contener infromación, solo un status code.
Las "respuestas" deberan consistir de otro mensaje HTTP.

===msg 3ero<-->biz
No siempre se puede controlar la arquitectura, deberá ser lo más parecida posible a msg<-->biz


===client<->biz
No

== Polling
Si un servidor msg, tuviera una conexión directa con un msg3, puede enviar los mensajes de biz tal como los recibe sin almacenarlos.
Si un servidor msg se conecta directamente con el cliente, deberá almacenar los mensajes de biz hasta que sean pedidos por client, en ese momento los destruirá.


