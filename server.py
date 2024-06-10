import socket
import threading
import pickle
import time
import random
import constants as c

from sprites import Sprites
from collections import defaultdict

def spawn_random():
    x = random.randint(0, c.MAP_WIDTH-1) + 0.5
    y = random.randint(0, c.MAP_HEIGHT-1) + 0.5
    while c.game_map[int(x)][int(y)] != 0:
        x = random.randint(0, c.MAP_WIDTH-1) + 0.5
        y = random.randint(0, c.MAP_HEIGHT-1) + 0.5
    return x, y

def calculate_distance(a, b):
        return ((a.x - b.x)**2 + (a.y - b.y)**2)**(0.5)

def check_death(my_id, dict_sprites):
    my_sprite = None
    for player_id, sprites_list in dict_sprites.items():
        if int(player_id) == my_id:
            for sprite in sprites_list:
                if sprite.is_player:
                    my_sprite = sprite
    
    for player_id, sprites_list in dict_sprites.items():
        if int(player_id) != my_id:
            for sprite in sprites_list:
                if not sprite.is_player:
                    if calculate_distance(my_sprite, sprite) < 0.4:
                        #print("Death distance: {}".format(calculate_distance(my_sprite, sprite)))
                        return player_id
    return False

def threaded_client(conn, _id):
    global sprites_dict, connections, message

    current_id = _id

    
    data = conn.recv(16)                                                #Se reciben datos del cliente
    name = data.decode("utf-8")
    print("[SERVER]", name, "connected to the server.")


    conn.send(str.encode(str(current_id)))                                                  #Se crea instancia de un jugador nuevo al enviar id del cliente
    sprites_dict[current_id].append(Sprites(1, 1, 1, 1, None, 0, True, 2, 1, 0, name))
    message[current_id] = ""                                                                #Se envía ID al cliente
    scoreboard[current_id] = [0, 0]
    for key in message.keys():
        message[key] = "{} connected to the server".format(name).upper()

    while True:                                                                            #Loop principal para gestión de datos
        for player_id, sprites in sprites_dict.items():
            for sprite in sprites:
                sprite.move()
                if c.game_map[int(sprite.x)][int(sprite.y)] and not sprite.is_player:
                    sprites_dict[player_id].remove(sprite)

        death_info = [0, 0]                                                             #Si se registra una eliminación, se cambia información de la tqabla de posiciones y se crea un nuevo punto de reapaarición
        killer = check_death(current_id, sprites_dict)
        if killer:
            death_info = spawn_random()
            for player_id, sprites in sprites_dict.items():
                for sprite in sprites:
                    if sprite.is_player and player_id == killer:
                        name1 = sprite.name
                        scoreboard[int(player_id)][0] += 1
                    if sprite.is_player and int(player_id) == current_id:
                        name2 = sprite.name
                        scoreboard[int(player_id)][1] += 1
            for key in message.keys():
                message[key] = "{} killed {}".format(name1, name2).upper()

        try:
            send_data = pickle.dumps((sprites_dict, death_info, message[current_id], scoreboard))       #Se sigue informando de posición de jugador al cliente
            message[current_id] = ""
            conn.send(send_data)
            
        except Exception as e:
            print(e)
        
        try:
            data = conn.recv(2048)                                                                      #Se reciben datos del cliente
            if not data:
                break
            x, y, projectile_data = pickle.loads(data)                                                  #Datos de proyectiles

            
            if data:
                for player_id, sprites in sprites_dict.items():                                         #Posición del jugador
                    if int(player_id) == current_id:
                        for sprite in sprites:
                            if sprite.is_player:
                                sprite.x = x
                                sprite.y = y
                if projectile_data:
                    sprites_dict[current_id].append(projectile_data)
        except Exception as e:
            break  # if an exception has been reached disconnect client       
        time.sleep(0.001)

    
    print("[SERVER] Name:", name, ", Client Id:", current_id, "disconnected")                           #Mensaje del servidor
    for key in message.keys():
        message[key] = "{} desconectado".format(name).upper()
    connections -= 1 
    del sprites_dict[current_id]  # remove client information from players list
    conn.close()  # close connection


#============================================================================================================

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                   #Configuración de sockets
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


PORT = 5000                                                                                             #puerto a utilizar
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)


try:                                                                                                    #Se conecta al servidor
    S.bind(('172.30.34.108', PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] El servidor no pudo iniciarse")
    quit()

S.listen()                                                                                              #Espera conexiones

print("[SERVER] Se inicializó el servidor en: local ip {}  puerto {}".format(SERVER_IP, PORT))


sprites_dict = defaultdict(list)                                                        #Variables dinámicas
connections = 0
_id = 1
threads = []
message = {}
scoreboard = {}

print("[SERVER] Esperando a conexiones...")


while True:                                                                             #Se debe embuclar hasta tener conexiones
    host, addr = S.accept()
    print("[SERVER] Conectado a: {}".format(addr))
    connections += 1
    
    t = threading.Thread(target=threaded_client,args=(host,_id))                        #Se crea un hilo de juego para cada jugador
    t.start()
    _id += 1

print("[SERVER] Servidor fuera de línea")