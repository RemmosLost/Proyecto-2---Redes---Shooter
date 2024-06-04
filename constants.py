# Algunos colores a utilizar
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)

#Dimenciones de formatos
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
TEX_WIDTH = 64
TEX_HEIGHT = 64
MAP_WIDTH = 32
MAP_HEIGHT = 32

#Matriz representativa del laberinto
game_map = (
    (8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8),
    (8,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,6,6,6,6,0,0,0,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,0,0,8),
    (8,0,6,0,0,6,0,0,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,6,0,0,8),
    (8,0,6,0,0,6,0,0,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,6,0,0,8),
    (8,0,6,6,6,6,0,0,0,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,7,7,7,7,0,0,0,7,7,7,7,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,6,6,6,6,0,0,0,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,0,0,8),
    (8,0,6,0,0,6,0,0,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,6,0,0,8),
    (8,0,6,0,0,6,0,0,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,6,0,0,8),
    (8,0,6,6,6,6,0,0,0,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,7,7,7,7,0,0,0,7,7,7,7,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,2,0,0,2,6,6,6,6,6,6,0,0,0,8,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,2,0,0,2,6,6,6,6,6,6,0,0,0,8,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,8),
    (8,7,7,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,2,0,0,2,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,8),
    (8,0,7,7,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,7,7,0,8,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8,0,0,0,0,0,0,0,8),
    (8,0,0,0,6,6,6,6,6,6,0,0,0,0,6,6,6,6,6,6,0,0,0,8,0,0,0,0,0,0,0,8),
    (8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,8),
    (8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8)
)
