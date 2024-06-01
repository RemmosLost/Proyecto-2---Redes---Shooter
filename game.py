import pygame
import pickle
from math import floor, sin, cos, pi

from sprites import Sprites
from spriteSheet import SpriteSheet

class Game:
    def __init__(self):
        '''
        Constructor: guarda información del juego, así como el plano del motor de raycasting
        Entradas: N/A
        Salidas N/A
        Restricciones: N/A
        '''

        
        self.posX = 3.0                                     #Posición por defecto del Jugador
        self.posY = 10.0 

        
        self.dirX = -1.0                                    #Vector de Distancia
        self.dirY = 0.0 
        
        self.planeX = 0.0                                   #Configuración de perspectiva de cámara de Raycaster
        self.planeY = 0.66


        self.sprites = {}                                   #Diccionario que guarda las instancias de sprites 
        self.textures = []                                  #Se añaden las texturas que se van a usar en el juego
        
        #--------Se cargan texturas, Nota: Si quieren podemos cambiarlos por otros, por ahora tiene los default de la página.
        self.textures.append(SpriteSheet("assets/eagle.png")) #1        
        self.textures.append(SpriteSheet("assets/redbrick.png")) #2
        self.textures.append(SpriteSheet("assets/purplestone.png")) #3
        self.textures.append(SpriteSheet("assets/greystone.png")) #4
        self.textures.append(SpriteSheet("assets/bluestone.png")) #5
        self.textures.append(SpriteSheet("assets/mossy.png")) #6
        self.textures.append(SpriteSheet("assets/wood.png")) #7
        self.textures.append(SpriteSheet("assets/colorstone.png")) #8
        self.projectile_image = SpriteSheet("assets/projectile.png")
        self.player_image = SpriteSheet("assets/player.png")
        self.floor_img = pygame.image.load("assets/floor.png").convert()
        

        
        
        self.font = pygame.font.Font('freesansbold.ttf', 10)                                #Instancias de parámetrosdel juego
        self.font_large = pygame.font.Font('freesansbold.ttf', 26)
        self.time = 0                                                                       #Tiempo de Frame actual     
        self.oldTime = 0                                                                   #Tiempo de Frame anterior
        self.frameTime = 0.0
        self.my_id = -1                                                                     #Guarda Id del jugador
        self.sprites[self.my_id] = []

        #==Parámetros de Juego==

        self.shoot = False
        self.is_connected = False
        self.done = False
        
        self.message = ""
        self.old_message_time = 0
        self.message_time = 0
        self.scoreboard_data = {}                                                   
        self.zBuffer = []
        self.show_cursor = False

        #self.game_map = c.game_map
        self.show_scoreboard = False
        #self.scoreboard = Scoreboard()

