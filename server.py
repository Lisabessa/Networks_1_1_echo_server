import socket
from threading import Lock, Thread


def handle_client(sock, clients, lock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if not data:
                continue

            if data.lower() == b'exit':
                with lock:
                    if addr in clients:
                        clients.remove(addr)
                print(f"Клиент {addr} отключен.")

            msg = f"[{addr[0]}:{addr[1]}]: {data.decode()}"
            print(msg)

            with lock:
                for client_addr in clients:
                    sock.sendto(msg.encode(), client_addr)

        except Exception as e:
            print(f"Ошибка с клиентом {addr}: {e}")


def run_echo_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('192.168.0.17', 9090))
    print("Сервер запущен на порту 9090")

    clients = []
    lock = Lock()
    
    Thread(target=handle_client, args=(sock, clients, lock), daemon=True).start()

    while True:
        _, addr = sock.recvfrom(1024)
        with lock:
            if addr not in clients:
                clients.append(addr)
                print(f"Новое подключение: {addr}")


run_echo_server()