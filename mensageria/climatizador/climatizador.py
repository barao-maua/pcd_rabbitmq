import pika

hostname = "rabbit" # colocar localhost para rodar sem docker e rabbit para rodar com docker
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
channel = connection.channel()

channel.exchange_declare(exchange='alerta_temperatura_alta', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='alerta_temperatura_alta', queue=queue_name)

print(' [*] Waiting for alerts. To exit press CTRL+C')

def acionar_climatizador(ch, method, properties, body):
    print(" [x] Acionando climatizador - Temperatura de: %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=acionar_climatizador, auto_ack=True)

channel.start_consuming()

