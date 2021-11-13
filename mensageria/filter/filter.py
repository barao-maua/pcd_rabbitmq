import pika, sys, os

def main():

    hostname = "rabbit" # colocar localhost para rodar sem docker e rabbit para rodar com docker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
    channel = connection.channel()

    channel.queue_declare(queue='temperatura')

    def checar_temperatura(ch, method, properties, body):
        temp = int(body)
        print(" [x] Temperatura recebida %r" % body)
        if( temp > 30 ):
            print("Temperatura maior que 30")
            channel.exchange_declare(exchange='alerta_temperatura_alta', exchange_type='fanout')
            channel.basic_publish(exchange='alerta_temperatura_alta', routing_key='', body=str(temp))
            print(" [x] Alerta temperatura %d" % temp)




    channel.basic_consume(queue='temperatura', on_message_callback=checar_temperatura, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)