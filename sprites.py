class Sprites():

    '''Clase que guarda información acerca de cada sprite así como información del jugador.'''

    def __init__(self, x, y, dir_x, dir_y, image, speed, is_player=False, uDiv=10, vDiv=10, vMove=60, name="JugadorX"):
        #====Datos del Sprite ====
        self.x = x                          #Coordenadas de posición en el mapa
        self.y = y                          
        self.image = image                  #asset del sprite
        

        #====Datos de Jugador====

        self.speed = speed                  #Velocidad de movimiento
        
        self.dir_x = dir_x                  #Dirección a la que ve el jugador
        self.dir_y = dir_y
        
        self.uDiv = uDiv
        self.vDiv = vDiv
        
        self.vMove = vMove                 #Parámetros
        self.is_player = is_player
        self.kills = 0                     #Cant de eliminaciones
        self.deaths = 0                    #Veces Eliminado
        self.name = name                   #Guarda nombre del jugador      
    
    def move(self):
        '''
        Función que modifica la posición del jugador
        Entradas: N/A
        Salidas: Posición actualizada.
        Restricciones: N/A
        '''
        self.x +=  self.dir_x*self.speed
        self.y += self.dir_y*self.speed