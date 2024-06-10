import pygame
import constants as c

class Minimap:
    """
        Constructor de la clase
        Entradas: * squera_size (int): el tamaño que será el minimapa
        Salidas N/A
        Restricciones: N/A

        Para la superficie se tomaran los valores del tamaño del mapa para dibujar el minimapa en proporcion a este.
    """
    def __init__(self, square_size):
        self.square_size = square_size
        self.surface = pygame.Surface((self.square_size*c.MAP_WIDTH, self.square_size*c.MAP_HEIGHT)).convert()
        self.x = c.SCREEN_WIDTH - self.square_size*c.MAP_WIDTH
        self.y = 0
        
    def draw(self, destination, world_map, player_x, player_y, dict_sprites):
        """
            Funcion para dibujar el minimapa en pantalla
           Entradas:    * destination (surface): superficie donde pygame dibujará el minimapa.
                        * wordl_map (tuple): contiene la informacion del mapa.
                        * player_x (float): posicion x del jugador en el juego.
                        * player_y (float): posicion y del jugador en el juego.
                        * dict_sprites (dict): diccionario de sprites que se mostraran en el minimapa.
        Salidas: N/A

        Nota:Para la superficie se tomaran los valores del tamaño del mapa para dibujar el minimapa en proporcion a este.
        """
        self.surface.fill(c.GRAY)
        for i, row in enumerate(world_map):
            for j, element in enumerate(row):
                if element:
                    pygame.draw.rect(self.surface, c.BLACK, (j*self.square_size, i*self.square_size,
                                                            self.square_size, self.square_size))

        ### Se dibuja el player en el minimapa como un punto segun sus cordenadas x, y
        dot_x = (player_x / c.MAP_WIDTH) * self.square_size * c.MAP_WIDTH
        dot_y = (player_y / c.MAP_HEIGHT) * self.square_size * c.MAP_HEIGHT
        pygame.draw.circle(self.surface, c.BLUE, (int(dot_y), int(dot_x)), self.square_size//2)

        ### Se dibujan los sprites del mapa completo en el minimapa
        for player_id, sprites_list in dict_sprites.items():
            for sprite in sprites_list:
                if not sprite.is_player:
                    dot_x = (sprite.x / c.MAP_WIDTH) * self.square_size * c.MAP_WIDTH
                    dot_x = (sprite.x / c.MAP_HEIGHT) * self.square_size * c.MAP_HEIGHT
                    pygame.draw.circle(self.surface, c.RED, (int(dot_y), int(dot_x)), self.square_size//2)
        destination.blit(self.surface, (self.x, self.y))
