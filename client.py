import pygame
import constants as c
import socket
import time
import pickle
import threading 
from sprites import Sprites
from game import Game



def network_data_handle():
    """ 
    Función que se encarga del control de datos en una red. Esta función trabaja como hilo para desacoplar el loop del juego de la gestión de datos.

    
    Entradas: N/A
    Salidas: Manejo de datos entre cliente y server
    Restricciones: N/A
    """
        
    global client, game
    while not game.done:
        try:
            data = client.recv(2048)
            sprites_dict_data, death_info, message, scoreboard_data = pickle.loads(data)
            if message:
                game.message = message
            
            for key, sprites in sprites_dict_data.items():
                for sprite in sprites:
                    if sprite.is_player:
                        sprite.image = game.player_image
                    else:
                        sprite.image = game.projectile_image
            if death_info[0] and death_info[1]:
                game.posX, game.posY = death_info
            game.sprites = sprites_dict_data.copy()
            game.scoreboard_data = scoreboard_data.copy()

        except Exception as e:
            print(e)
        try:
            projectile_data = 0
            if game.shoot:
                game.shoot = False
                projectile_data = Sprites(game.posX, game.posY, game.dirX, game.dirY, 0, 0.2)
            send_data = pickle.dumps((game.posX, game.posY, projectile_data))
            client.send(send_data)
        except Exception as e:
            print(e)
        time.sleep(0.001)
    client.close()

pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
clock = pygame.time.Clock()
game = Game()


pygame.mouse.set_visible(False)                                                         #Se oculta el mouse en la ventana de juego
pygame.event.set_grab(True)     


f = open("ConfiguracionLAN.txt", "r")                                                 #Lee archivo de texto con configuraciones de jugador
CONDITION, PLAYER_NAME, IP, PORT = f.read().splitlines()
print("1: {} 2: {} 3: {} 4: {}".format(CONDITION, PLAYER_NAME, IP, PORT))
if CONDITION == "YES" or CONDITION == "Yes" or CONDITION == "yes":
    game.is_connected = True
print("¿Conectado? {}".format(game.is_connected))
PORT = int(PORT)
f.close()


if game.is_connected:                                                       #Si se conecta al server, se crea la conexión y se envían y reciben datos del cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (IP, PORT)
    client.connect(addr)
    client.send(str.encode(PLAYER_NAME))
    val = client.recv(8)
    print("Received id: {}".format(val.decode()))
    game.my_id = int(val)
    t = threading.Thread(target=network_data_handle)
    t.start()

# Main loop
while not game.done:
    events = pygame.event.get()
    game.draw(screen)
    game.input_handle()
    pygame.display.flip()
    clock.tick()
pygame.quit()