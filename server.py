import selectors
import socket
import time
import hashlib
import random
import sys
import signal
import ast

sel = selectors.DefaultSelector()

HOST, PORT = sys.argv[1],  int(sys.argv[2])
server_address = (HOST, PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(1000)
users = ast.literal_eval(open('info.txt', 'r').read())

print(f"Ванна запущена на: {server_address}")

sel.register(server_socket, selectors.EVENT_READ, data=None)


client_data = {}
rooms = {}


def accept_client(sock):
    client_socket, client_address = sock.accept()
    print(f"[{time.strftime('%H:%M:%S')}] Новый крокодил зашел в ванную: {client_address}")
    client_socket.sendall('Крокодил. Если ты хочешь зарегестрироватся в чатике напиши: /register <username> <password>.\n Если ты хочешь войти в чатик напиши: /login <username> <password>\n'.encode())
    sel.register(client_socket, selectors.EVENT_READ, handle_client)
    client_data[client_socket] = {"id": len(client_data), "buffer": b""}


def handle_client(sock):
    client_id = client_data[sock]["id"]
    data = sock.recv(1024)
    if data:
        client_data[sock]["buffer"] += data
        message_end = client_data[sock]["buffer"].find(b"\n")
        if message_end != -1:
            message = client_data[sock]["buffer"][:message_end].decode().strip()
#---------------------------------------------------------------------------  
            if message.startswith('/login'):
                # User login
              try:
                _, username, password = message.split(' ')
                if username in users and users[username]['password'] == hashlib.sha256(password.encode()).hexdigest():
                  client_data[sock]['username'] = username
                  sock.sendall('Вы успешно вошли в систему!\n'.encode())
                  sock.sendall('Крокодил.\n Если ты хочешь создать комнату в чатике напиши: /create <room_name>.\n Если ты хочешь войти в комнату напиши: /join <room_name> <password>.\n Если ты хочешь покинуть комнату и вернутся в помойку напиши: /exit.\n'.encode())
                  client_data[sock]['room'] = 'flood'
                else:
                    sock.sendall('Неверное имя пользователя или пароль.\n'.encode())
              except:
                  sock.sendall('Попробуйте ввести вашу бибу еще раз'.encode())
#---------------------------------------------------------------------------  
            elif message.startswith('/register'):
                # User registration
              try:
                _, username, password = message.split(' ')
                if username in users:
                    sock.sendall('Это имя пользователя уже занято.\n'.encode())
                else:
                    users[username] = {'password': hashlib.sha256(password.encode()).hexdigest()}
                    client_data[sock]['username'] = username
                    sock.sendall('Вы успешно зарегистрировались!\n'.encode())
                    client_data[sock]['room'] = 'flood'
              except:
                sock.sendall('Попробуйте ввести вашу бибу еще раз'.encode())
#---------------------------------------------------------------------------  
            elif message.startswith('/create'):
                # Create a room
              try:
                _, room_name = message.split(' ')
                if room_name in rooms:
                    sock.sendall(f'Комната {room_name} уже создана. Пожалуйста, выберите другое имя.\n'.encode())
                else:
                    password = random.randint(1000, 5000)
                    rooms[room_name] = {'password': password, 'members': {client_data[sock]['username']}}
                    client_data[sock]['room'] = room_name
                    sock.sendall(f'Комната {room_name} создана. Пароль: {password}\n'.encode())
              except:
                sock.sendall('Попробуйте ввести вашу бибу еще раз'.encode())
#---------------------------------------------------------------------------  
            elif message.startswith('/join'):
                # Join a room
              try:
                _, room_name, password = message.split(' ')
                if room_name not in rooms:
                    sock.sendall(f'Комната {room_name} не существует. Пожалуйста, выберите другую комнату.\n'.encode())
                elif int(rooms[room_name]['password']) != int(password):
                    sock.sendall(f'Неверный пароль для комнаты {room_name}.\n'.encode())
                else:
                    rooms[room_name]['members'].add(client_data[sock]['username'])
                    client_data[sock]['room'] = room_name
                    sock.sendall(f'Вы вошли в комнату {room_name}.\n'.encode())
              except:
                sock.sendall('Попробуйте ввести вашу бибу еще раз'.encode())
#---------------------------------------------------------------------------  
            elif message.startswith('/exit'):
                # Exit a room
              try:
                if 'flood' in client_data[sock]['room']:
                    sock.sendall('Вы не находитесь в комнате.\n'.encode())
                else:
                    room_name = client_data[sock]['room']
                    rooms[room_name]['members'].discard(client_data[sock]['username'])
                    del client_data[sock]['room']
                    client_data[sock]['room'] = 'flood'
                    sock.sendall(f'Вы вышли из комнаты {room_name} и вернулись в главный чат.\n'.encode())
              except:
                sock.sendall('Попробуйте ввести вашу бибу еще раз'.encode())
#---------------------------------------------------------------------------  
            else:
              if 'username' in client_data[sock]:
                if 'flood' in client_data[sock]['room']:
                  broadcast_room(f"[{time.strftime('%H:%M:%S')}] {client_data[sock]['username']}: {message}\n", client_data[sock]['room'])
                  print(f"[{time.strftime('%H:%M:%S')}] Крокодил {client_data[sock]['username']} говорит: {message}")
                else:
                  broadcast_room(f"[{time.strftime('%H:%M:%S')}] {client_data[sock]['username']}: {message}\n", client_data[sock]['room'])
              else:
                  sock.sendall('Пожалуйста, войдите в систему, чтобы продолжить.\n'.encode())
            client_data[sock]["buffer"] = client_data[sock]["buffer"][message_end + 1:]
    else:            
      print(f"[{time.strftime('%H:%M:%S')}] ААААА Крокодил {client_data[sock]['username']} вышел из ванной.")
      broadcast_room(f"[{time.strftime('%H:%M:%S')}] ААААА Крокодил {client_id} вышел из ванной.\n", client_data[sock]['room'])
      sel.unregister(sock)
      del client_data[sock]
      sock.close()
          
def broadcast_room(message, current_room):
  for sock in client_data.keys():
    if current_room in client_data[sock]['room']:
      sock.sendall(message.encode())


def save_users(signum, frame):
  global users
  print(users,file=open('info.txt', 'w'))
  exit(0)
  

signal.signal(signal.SIGINT, save_users)
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_client(key.fileobj)
        else:
            handle_client(key.fileobj)
