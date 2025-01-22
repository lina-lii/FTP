import socket

HOST = 'localhost'
PORT = 9090

def start_client():
    """Запуск клиента"""
    while True:
        sock = socket.socket()
        sock.connect((HOST, PORT))
        
        # Вводим команду
        request = input('myftp@shell$ ')
        
        if request == 'exit':
            sock.send(request.encode())
            print('Выход из программы')
            sock.close()
            break
        
        sock.send(request.encode())
        
        # Получаем ответ
        response = sock.recv(1024).decode()
        print(response)
        
        sock.close()

start_client()