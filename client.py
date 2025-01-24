import socket
from threading import Thread


def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(data.decode())
        except Exception as e:
            print(f"Ошибка с клиентом: {e}")
            break


def client_connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input('Введите сообщение:\n')
        client_socket.sendto(message.encode(), ('192.168.0.17', 9090))
        if message.lower() == 'exit':
            break

    client_socket.close()


client_connect()