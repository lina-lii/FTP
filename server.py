import socket
import os
import shutil

PORT = 9090
WORK_DIR = 'server_dir'  # Рабочая директория сервера

# Убедимся, что рабочая директория существует
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)

def process_request(request):
    """Обработка команд клиента"""
    command = request.split()
    
    if not command:
        return 'bad request'

    cmd = command[0]
    
    if cmd == 'pwd':
        # Выводит текущую директорию
        return os.getcwd()

    elif cmd == 'ls':
        # Просмотр содержимого папки
        folder = command[1] if len(command) > 1 else WORK_DIR
        try:
            return '\n'.join(os.listdir(folder))
        except FileNotFoundError:
            return 'Folder not found'
    
    elif cmd == 'mkdir':
        # Создать папку
        folder_name = command[1] if len(command) > 1 else None
        if folder_name:
            os.makedirs(os.path.join(WORK_DIR, folder_name), exist_ok=True)
            return f'Folder {folder_name} created'
        else:
            return 'Bad request: folder name missing'

    elif cmd == 'rmdir':
        # Удалить папку
        folder_name = command[1] if len(command) > 1 else None
        if folder_name:
            folder_path = os.path.join(WORK_DIR, folder_name)
            try:
                shutil.rmtree(folder_path)
                return f'Folder {folder_name} removed'
            except FileNotFoundError:
                return 'Folder not found'
        else:
            return 'Bad request: folder name missing'

    elif cmd == 'rm':
        # Удалить файл
        file_name = command[1] if len(command) > 1 else None
        if file_name:
            try:
                os.remove(os.path.join(WORK_DIR, file_name))
                return f'File {file_name} removed'
            except FileNotFoundError:
                return 'File not found'
        else:
            return 'Bad request: file name missing'

    elif cmd == 'rename':
        # Переименовать файл
        old_name = command[1] if len(command) > 1 else None
        new_name = command[2] if len(command) > 2 else None
        if old_name and new_name:
            try:
                os.rename(os.path.join(WORK_DIR, old_name), os.path.join(WORK_DIR, new_name))
                return f'File {old_name} renamed to {new_name}'
            except FileNotFoundError:
                return 'File not found'
        else:
            return 'Bad request: missing file names'

    elif cmd == 'copy_to_server':
        # Принимаем файл от клиента и сохраняем на сервере
        file_name = command[1] if len(command) > 1 else None
        file_content = request.split('\n', 1)[1]  # Содержимое файла

        if file_name:
            with open(os.path.join(WORK_DIR, file_name), 'w') as file:
                file.write(file_content)
            return f'File {file_name} copied to server'
        else:
            return 'Bad request: file name missing'
    
    elif cmd == 'exit':
        return 'exit'
    
    else:
        return 'Bad request'

def start_server():
    """Запуск сервера"""
    sock = socket.socket()
    sock.bind(('', PORT))
    sock.listen(5)

    print(f"Слушаем порт {PORT}")
    
    while True:
        conn, addr = sock.accept()
        print(f"Подключение от {addr}")
        
        request = conn.recv(1024).decode()
        print(f"Получен запрос: {request}")
        
        response = process_request(request)
        
        conn.send(response.encode())
        conn.close()

start_server()