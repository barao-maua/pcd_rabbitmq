import pika
import time
import random

def main():
    hostname = "rabbit" # colocar localhost para rodar sem docker e rabbit para rodar com docker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
    channel = connection.channel()
    temperatura = str(random.randint(10,40))
    print("Temperatura é de ", temperatura)

    channel.queue_declare(queue='temperatura')

    channel.basic_publish(exchange='',
                      routing_key='temperatura', # nome da fila
                      body=temperatura)
    connection.close()

if __name__ == '__main__':
    while(True):
        try:
            main()
            time.sleep(20)
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


