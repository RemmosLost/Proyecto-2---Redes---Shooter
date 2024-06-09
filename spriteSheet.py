import pygame
# import constants as constants

class SpriteSheet (object):
    """
    Constructor de la clase
    Entradas: * file_name (String): nombre del archivo que se cargará
    Salidas N/A
    Restricciones: N/A
    """
    def __int__(self, file_name):
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()


    def get_image(self, x, y, width, heigth):
        """
        Funcion para obtener una imagen
        Entradas:   * x     (int) : la posicion en X de la imagen solicitada
                    * y     (int) : la posicion en Y de la imagen solicitada
                    * width (int) : el ancho de la imagen solicitada
                    * height (int) : la altura de la imagen solicitada
        Salidas: la imagen que contiene las partes solicitadas.
        Restricciones: N/A
        """
        image = pygame.Surface([width, heigth], pygame.SRCALPHA).convert_alpha()
        image.blit(self.sprite_sheet, (0,0), (x, y, width, heigth))
        return image


    def get_width(self):
        """
          Funcion para obtener la anchura de una imagen
          Salidas: int (width)
        """
        return self.sprite_sheet.get_width()

    def get_height(self):
        """
            Funcion para obtener la altura de una imagen
            Salidas: int (height)
        """
        return self.sprite_sheet.get_height()