import pygame
import pickle
from math import floor, sin, cos, pi

from sprites import Sprites
from spriteSheet import SpriteSheet
from minimap import Minimap
from scoreboard import Scoreboard
import constants as c


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

        self.textures.append(SpriteSheet("assets/bronze2.png")) #1        
        self.textures.append(SpriteSheet("assets/steel2.png")) #2
        self.textures.append(SpriteSheet("assets/stones.png")) #3
        self.textures.append(SpriteSheet("assets/bronze.png")) #4
        self.textures.append(SpriteSheet("assets/steel.png")) #5
        self.textures.append(SpriteSheet("assets/bricks.png")) #6
        self.textures.append(SpriteSheet("assets/yellowstone.png")) #7
        self.textures.append(SpriteSheet("assets/colorstone.png")) #8
        self.projectile_image = SpriteSheet("assets/projectile.png")
        self.player_image = SpriteSheet("assets/player.png")
        self.floor_img = pygame.image.load("assets/floor.png").convert()
        
        self.minimap = Minimap(5)
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

        self.game_map = c.game_map                                                      #Se instancian mapas y tabla depuntuaciones
        self.show_scoreboard = False
        self.scoreboard = Scoreboard()


    def input_handle(self):                                                 
            """ Función que capta los movimientos del mouse y del teclado
            Entradas: N/A
            Salidas: Posición actualizada del jugador sobre el mapa.
            Restricciones: N/A
            """        
            events = pygame.event.get()                                                     #Se registran eventos de dispositivos.

            #Modificadores de velocidad
            moveSpeed = self.frameTime * 5.0            # Velocidad de movimiento del jugador
            rotSpeed = self.frameTime * 3.0             # Velocidad de rotación del jugador

            key = pygame.key.get_pressed()                                                  #Se registran teclas presionadas.
            
            if key[pygame.K_w]:                                                             
                if(self.game_map[int(self.posX + self.dirX * moveSpeed)][int(self.posY)] == False):         #Sepuede mover al frente siempre y cuando no hayan paredes
                    self.posX += self.dirX * moveSpeed
                if(self.game_map[int(self.posX)][int(self.posY + self.dirY * moveSpeed)] == False):
                    self.posY += self.dirY * moveSpeed

            
            if key[pygame.K_s]:
                if(self.game_map[int(self.posX - self.dirX * moveSpeed)][int(self.posY)] == False):         #Sepuede mover a atrás siempre y cuando no hayan paredes    
                    self.posX -= self.dirX * moveSpeed
                if(self.game_map[int(self.posX)][int(self.posY - self.dirY * moveSpeed)] == False):
                    self.posY -= self.dirY * moveSpeed
            
            if key[pygame.K_d]:
                oldDirX = self.dirX                                                                 
                self.dirX = self.dirX * cos(-pi/2) - self.dirY * sin(-pi/2)
                self.dirY = oldDirX * sin(-pi/2) + self.dirY * cos(-pi/2)
                oldPlaneX = self.planeX
                self.planeX = self.planeX * cos(-pi/2) - self.planeY * sin(-pi/2)
                self.planeY = oldPlaneX * sin(-pi/2) + self.planeY * cos(-pi/2)

                if(self.game_map[int(self.posX + self.dirX * moveSpeed)][int(self.posY)] == False):             #Se puede mover a la derecha si no hay paredes
                    self.posX += self.dirX * (moveSpeed/2)
                if(self.game_map[int(self.posX)][int(self.posY + self.dirY * moveSpeed)] == False):
                    self.posY += self.dirY * (moveSpeed/2)


                #debe moverse el POV de la cámara
                oldDirX = self.dirX
                self.dirX = self.dirX * cos(pi/2) - self.dirY * sin(pi/2)
                self.dirY = oldDirX * sin(pi/2) + self.dirY * cos(pi/2)
                oldPlaneX = self.planeX
                self.planeX = self.planeX * cos(pi/2) - self.planeY * sin(pi/2)
                self.planeY = oldPlaneX * sin(pi/2) + self.planeY * cos(pi/2)
            
            if key[pygame.K_a]:
                oldDirX = self.dirX
                self.dirX = self.dirX * cos(-pi/2) - self.dirY * sin(-pi/2)
                self.dirY = oldDirX * sin(-pi/2) + self.dirY * cos(-pi/2)
                oldPlaneX = self.planeX
                self.planeX = self.planeX * cos(-pi/2) - self.planeY * sin(-pi/2)
                self.planeY = oldPlaneX * sin(-pi/2) + self.planeY * cos(-pi/2)

                if(self.game_map[int(self.posX - self.dirX * moveSpeed)][int(self.posY)] == False):              #Se puede mover a la izquierda si no hay paredes       
                    self.posX -= self.dirX * moveSpeed
                if(self.game_map[int(self.posX)][int(self.posY - self.dirY * moveSpeed)] == False):
                    self.posY -= self.dirY * moveSpeed

                #debe moverse el POV de la cámara
                oldDirX = self.dirX
                self.dirX = self.dirX * cos(pi/2) - self.dirY * sin(pi/2)
                self.dirY = oldDirX * sin(pi/2) + self.dirY * cos(pi/2)
                oldPlaneX = self.planeX
                self.planeX = self.planeX * cos(pi/2) - self.planeY * sin(pi/2)
                self.planeY = oldPlaneX * sin(pi/2) + self.planeY * cos(pi/2)



            #Rotación de POV de la cámara

            
            if key[pygame.K_RIGHT]:                                                 #Rotación a la derecha
                #Debe rotar el POV de la cámara
                oldDirX = self.dirX
                self.dirX = self.dirX * cos(-rotSpeed) - self.dirY * sin(-rotSpeed)
                self.dirY = oldDirX * sin(-rotSpeed) + self.dirY * cos(-rotSpeed)
                oldPlaneX = self.planeX
                self.planeX = self.planeX * cos(-rotSpeed) - self.planeY * sin(-rotSpeed)
                self.planeY = oldPlaneX * sin(-rotSpeed) + self.planeY * cos(-rotSpeed)

            
            if key[pygame.K_LEFT]:                                                  #Rotación a la izquierda
                #Debe rotar el POV de la cámara
                oldDirX = self.dirX
                self.dirX = self.dirX * cos(rotSpeed) - self.dirY * sin(rotSpeed)
                self.dirY = oldDirX * sin(rotSpeed) + self.dirY * cos(rotSpeed)
                oldPlaneX = self.planeX
                self.planeX = self.planeX * cos(rotSpeed) - self.planeY * sin(rotSpeed)
                self.planeY = oldPlaneX * sin(rotSpeed) + self.planeY * cos(rotSpeed)

            for event in events:            #Se registran movimiento del Mouse
                if event.type == pygame.QUIT:
                    self.done = True  
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if key[pygame.K_SPACE]:
                        self.shoot = True
                        if not self.is_connected:
                            self.sprites[self.my_id].append(Sprites(self.posX, self.posY, self.dirX, self.dirY, self.projectile_image, 0.4))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.shoot = True
                        if not self.is_connected:
                            self.sprites[self.my_id].append(Sprites(self.posX, self.posY, self.dirX, self.dirY, self.projectile_image, 0.4))
                    if event.button == 3:
                        if not self.show_cursor:
                            pygame.mouse.set_visible(True)
                            pygame.event.set_grab(False)
                            self.show_cursor = True
                        elif self.show_cursor:
                            pygame.mouse.set_visible(False)
                            pygame.event.set_grab(True)
                            self.show_cursor = False
                
            
            if key[pygame.K_ESCAPE]:
                self.done = True
                pygame.quit()

            self.show_scoreboard = False
            if key[pygame.K_TAB]:
                self.show_scoreboard = True
            
            (movement_x, movement_y) = pygame.mouse.get_rel()
            if movement_x:
                rotSpeed *= (-movement_x/25)
                oldDirX = self.dirX
                self.dirX = self.dirX * cos(rotSpeed) - self.dirY * sin(rotSpeed)
                self.dirY = oldDirX * sin(rotSpeed) + self.dirY * cos(rotSpeed)
                oldPlaneX = self.planeX
                self.planeX = self.planeX * cos(rotSpeed) - self.planeY * sin(rotSpeed)
                self.planeY = oldPlaneX * sin(rotSpeed) + self.planeY * cos(rotSpeed)


    def cast_sprites(self, dict_sprites, screen):                       ############FALTA ESTA CLASE
            """ Función que transmite y ordena los sprites del almacenamiento y los dibuja en la pantalla.
            Entradas:
                dict_sprites: Diccionario con todos los sprites del juego, incluyendo al jugador y proyectiles.
                screen (surface): Pantalla donde se dibujan los sprites.
            Salidas: Sprites cargados en memoria y dibujados en la cámara de juego
            Restricciones: N/A
            """        

            sprites = []

            
            for player_id, sprites_list in dict_sprites.items():    #Se debe evitar mostrarse a uno mismo en pantalla, solo jugadores rivales.
                for sprite in sprites_list:
                    if not (int(player_id) == self.my_id and sprite.is_player):
                        sprites.append(sprite)

            
            for sprite in sprites:                                 #Se proyectan todos los sprites y se dibujan de acuerdo a posición de la cámara.
                
                spriteX = sprite.x - self.posX
                spriteY = sprite.y - self.posY

                #Se transforma el sprite de acuerdo a la matriz invertida del la cámara. La cámara funciona de la siguiente materia.

                # [ planeX   dirX ] -1                                       [ dirY      -dirX ]
                # [               ]       =  1/(planeX*dirY-dirX*planeY) *   [                 ]
                # [ planeY   dirY ]                                          [ -planeY  planeX ]

                invDet = 1.0 / (self.planeX * self.dirY - self.dirX * self.planeY)              #Multiplicación de matrices, Nota: No Toquen esto!

                transformX = invDet * (self.dirY * spriteX - self.dirX * spriteY)
                transformY = invDet * (-self.planeY * spriteX + self.planeX * spriteY)          #Los sprites se reescalan de acuerdo a cercanía

                if transformY == 0:
                    transformY = 0.001
                spriteScreenX = int((c.SCREEN_WIDTH / 2) * (1 + transformX / transformY))

                

                uDiv = sprite.uDiv                                                          #Reescalado y movimiento de sprites
                vDiv = sprite.vDiv
                vMove = sprite.vMove
                    
                vMoveScreen = int(vMove / transformY)

                
                spriteHeight = abs(int(c.SCREEN_HEIGHT / (transformY))) / vDiv #Se calcula la "altura" del sprite en pantalla. Se usa "transformY" para evitar efecto de ojo de pez
                
                #Luego, se calcula el tamaño de acuerdo a la distancia de la línea actual renderizada
                
                drawStartY = -spriteHeight / 2 + c.SCREEN_HEIGHT / 2 + vMoveScreen
                if drawStartY < 0:
                    drawStartY = 0
                drawEndY = spriteHeight / 2 + c.SCREEN_HEIGHT / 2 + vMoveScreen
                if drawEndY >= c.SCREEN_HEIGHT:
                    drawEndY = c.SCREEN_HEIGHT - 1

                #Luego se calcula el ancho del cada sprite.
                spriteWidth = abs( int (c.SCREEN_HEIGHT / (transformY))) / uDiv
                drawStartX = -spriteWidth / 2 + spriteScreenX
                drawEndX = spriteWidth / 2 + spriteScreenX
                if drawEndX >= c.SCREEN_WIDTH:
                    drawEndX = c.SCREEN_WIDTH - 1

                
                image_width = sprite.image.get_width()                                  # Para cada sprite se obtienen sus dimensiones
                image_height = sprite.image.get_height()
                for stripe in range(int(drawStartX), int(drawEndX)):
                    texX = int(256 * (stripe - (-spriteWidth / 2 + spriteScreenX)) * image_width / spriteWidth) / 256
                    if transformY > 0 and drawStartX >= 0 and drawEndX < c.SCREEN_WIDTH and transformY < self.zBuffer[stripe]:
                        tmp_image1 = sprite.image.get_image(int(round(texX)), 0, 1, image_height)
                        tmp_image = pygame.transform.scale(tmp_image1, (1, int(spriteHeight)))

                        
                        darken_percent = (1 - (spriteHeight*30/c.SCREEN_HEIGHT))        #Pequeño filtro para oscurecer sprites mientras más lejanos estén
                        dark = pygame.Surface(tmp_image.get_size(), pygame.SRCALPHA).convert_alpha()
                        darkness = (darken_percent*255)
                        if darkness > 255:
                            darkness = 255
                        elif darkness < 0:
                            darkness = 0
                        dark.blit(tmp_image, (0 , 0))
                        dark.fill((darkness, darkness, darkness, 0), None, pygame.BLEND_RGBA_SUB)
                        #print("drawx: {} drawy: {}".format(drawStartX, drawStartY))
                        screen.blit(dark, (stripe , drawStartY))

                        middle_stripe = int(drawStartX + (drawEndX - drawStartX)//2)
                        if stripe ==  middle_stripe and sprite.is_player:
                            ratio = 4 * (spriteHeight / image_height) 
                            text_default = self.font_large.render(sprite.name, True, c.GREEN)
                            scaled_width = int(ratio*text_default.get_width())
                            scaled_height = int(ratio*text_default.get_height())
                            text = pygame.transform.scale(text_default, (scaled_width, scaled_height))
                            screen.blit(text, (middle_stripe  - text.get_width()//2, drawStartY - text.get_height()))


                # print("{}  {}  {}".format(drawEndX//2, drawStartY, inside))

                
                if not self.is_connected:
                    sprite.move()
                    if self.game_map[int(sprite.x)][int(sprite.y)]:
                        self.sprites[self.my_id].remove(sprite)




    def draw(self, screen):
            """Dibuja todos los componentes en pantalla.
            Entradas:
                screen (surface): pantala donde se dibuja el juego.
            Salidas: Dibujo en pantalla.
            Rrestricciones: N/A
            """        
            pygame.draw.rect(screen, c.BLACK, (0, 0, c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))
            floor_size = self.floor_img.get_size()
            if floor_size[0] != c.SCREEN_WIDTH or floor_size[1] != c.SCREEN_HEIGHT//2:
                self.floor_img = pygame.transform.scale(self.floor_img, (c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))
                self.floor_img.convert()
            screen.blit(self.floor_img, (0, c.SCREEN_HEIGHT//2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))

            self.zBuffer = []

            #Se deben trazar los rayos en busca de paredes, objetos y jugadores a mostrar
            for x in range(0, c.SCREEN_WIDTH):

                
                cameraX = 2 * x / c.SCREEN_WIDTH - 1                        # Se calcula la posición y dirección del rayo.        
                rayDirX = self.dirX + self.planeX*cameraX
                rayDirY = self.dirY + self.planeY*cameraX

                mapX = int(self.posX)                                       #Casilla del mapa en la que se encuentra el jugador actualemnte.s
                mapY = int(self.posY)

                
                sideDistX = 0.0                                             #Largo de cada rayo al próximo valor X o Y    
                sideDistY = 0.0

                
                
                if rayDirX == 0:                                            #Setter de largo del rayo desde un XoY a otro
                    rayDirX = 0.001
                if rayDirY == 0:
                    rayDirY = 0.001
                
                deltaDistX = abs(1 / rayDirX)
                deltaDistY = abs(1 / rayDirY)
                perpWallDist = 0.0

                stepX = -1                                                  #Dirección x o Y a caminar en el mapa (+1 o -1)
                stepY = -1

                hit = 0                                                     #Registra si hubo choque con pared
                side = 0                                                    #Registra si fue choque EW de pared.

                
                if rayDirX < 0:                                             #Se calcula paso inicial y distancia
                    stepX = -1
                    sideDistX = (self.posX - mapX) * deltaDistX
                else:
                    stepX = 1
                    sideDistX = (mapX + 1.0 - self.posX) * deltaDistX
                if rayDirY < 0:
                    stepY = -1
                    sideDistY = (self.posY - mapY) * deltaDistY
                else:
                    stepY = 1
                    sideDistY = (mapY + 1.0 - self.posY) * deltaDistY

                #Se ejecuta el algoritma DDA - Digital Differiential analyzer
                while hit == 0:
                    if sideDistX < sideDistY:   #Si no hay pared, salta a la siguiente posición X o Y
                        sideDistX += deltaDistX
                        mapX += stepX
                        side = 0
                    else:
                        sideDistY += deltaDistY
                        mapY += stepY
                        side = 1
                    
                    if(self.game_map[mapX][mapY] > 0):      #Se vuelve a preguntar si ahora si está tocando una pared
                        hit = 1

            
                if side == 0:                               #Se calcula la distancia del rayo perpendicular    (X e Y)                    
                    perpWallDist = (mapX - self.posX + (1 - stepX) / 2) / rayDirX
                else:
                    perpWallDist = (mapY - self.posY + (1 - stepY) / 2) / rayDirY

                
                if perpWallDist == 0:                           #Se calcula ahora la altura de la línea a dibujar en pantalla
                    perpWallDist = 0.000001
                lineHeight = int(c.SCREEN_HEIGHT / perpWallDist)
                if lineHeight > 10*c.SCREEN_HEIGHT:
                    lineHeight = 10*c.SCREEN_HEIGHT

                
                drawStart = -lineHeight / 2 + c.SCREEN_HEIGHT / 2   #Se dibuja el pixel más grande y pequeño del rayo 
                if drawStart < 0:
                    drawStart = 0
                drawEnd = lineHeight / 2 + c.SCREEN_HEIGHT / 2
                if drawEnd >= c.SCREEN_HEIGHT:
                    drawEnd = c.SCREEN_HEIGHT - 1

                #Se le agregan texturas al cálculo
                texNum = self.game_map[mapX][mapY] - 1  

                
                wallX = 0.0  #Se calcula la pared de PosX y se guarda la posición donde el rayo choca con ella                
                if side == 0:
                    wallX = self.posY + perpWallDist * rayDirY
                else:
                    wallX = self.posX + perpWallDist * rayDirX
                wallX -= floor((wallX))

                
                texX = int(wallX * c.TEX_WIDTH)         #Coordenada en X de la textura
                if(side == 0 and rayDirX > 0):
                    texX = c.TEX_WIDTH - texX - 1
                if(side == 1 and rayDirY < 0):
                    texX = c.TEX_WIDTH - texX - 1

                

                step = 1.0 * c.TEX_HEIGHT / lineHeight                                          #Se incrementa la coordinada de textura por cada pixel en patnalla
                
                texPos = (drawStart - c.SCREEN_HEIGHT / 2 + lineHeight / 2) * step              #Se obtiene la coordenada de la textura inicial

                image1 = self.textures[texNum].get_image(int(round(texX)), 0, 1, 64 )           #Se oscuren de acuerdo a distancia
                image2 = pygame.transform.scale(image1, (1, lineHeight))
                darken_percent = (1 - (lineHeight*5/c.SCREEN_HEIGHT))
                dark = pygame.Surface(image2.get_size()).convert_alpha()
                darkness = (darken_percent*255)
                if darkness > 255:
                    darkness = 255
                elif darkness < 0:
                    darkness = 0
                dark.fill((0, 0, 0, darkness))

                screen.blit(image2, ((x * 1), c.SCREEN_HEIGHT // 2 - lineHeight // 2))
                screen.blit(dark, ((x * 1), c.SCREEN_HEIGHT // 2 - lineHeight // 2))
                
                
                self.zBuffer.append(perpWallDist)                                               #Se inicializa la variable de Z para su transmisión de sprites


            self.cast_sprites(self.sprites, screen)                                             #se castean sprites de jugadores en pantalla
            
            
            self.minimap.draw(screen, self.game_map, self.posX, self.posY, self.sprites)        #Se dibujan Sprites del minimapa

            
            #Se registran entradas de teclado/mouse y contador de frames
            self.oldTime = self.time
            self.time = pygame.time.get_ticks()
            self.frameTime = (self.time - self.oldTime) / 1000.0 
            fps = 1.0 / self.frameTime
            text = self.font.render("FPS: {:.2f}".format(fps), True, c.WHITE)
            screen.blit(text, (10, 10))

            
            if self.show_scoreboard:                                                            #Se instancia y dibuja la tabla de posiciones
                self.scoreboard.draw(screen, self.sprites, self.scoreboard_data)

            
            cross_size = 20                                                                     #Se dibuja el crosshair
            pygame.draw.line(screen, c.RED, (c.SCREEN_WIDTH//2 - cross_size//2, c.SCREEN_HEIGHT//2 + 20),
                                (c.SCREEN_WIDTH//2 + cross_size//2, c.SCREEN_HEIGHT//2 + 20))
            pygame.draw.line(screen, c.RED, (c.SCREEN_WIDTH//2, c.SCREEN_HEIGHT//2 - cross_size//2 + 20),
                                (c.SCREEN_WIDTH//2, c.SCREEN_HEIGHT//2 + cross_size//2 + 20))

            
            
            if self.message:                                                                    #Se imprimen mensajes del servidor y se limpian cada cierto tiempo
                self.message_time = pygame.time.get_ticks()
                if self.message_time - self.old_message_time > 5000:
                    self.old_message_time = self.message_time
                    self.message = ""
            if not self.message:
                self.old_message_time = pygame.time.get_ticks()
            text = self.font.render(self.message, True, c.WHITE)
            screen.blit(text, (c.SCREEN_WIDTH//2, 10))   