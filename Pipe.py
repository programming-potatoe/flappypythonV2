import pygame
import os

from constants import HEIGHT, HIGHSCORE_NEW_PONIT, PIPE_WIDHT, WIDTH, PIPE_HOLE_SIZE, PIPE_SPEED, PIPE_LOWER, PIPE_UPPER

class Pipe(pygame.sprite.Sprite):
    """Class that contains the logic for pipe objects
    
    Attributes:
        hole_center: y coordinate of the center between the 2 pipes
        type: type of the pipe (upper or lower)
        image: the image of the pipe
        rect: the rect representation of the pipe
    """
    def __init__(self, type: int, hole_center: int) -> None:
        """Init function for the pipe class
        
        Args:
            type: the type of the pipe (upper or lower)
            hole_center: y coordinate of the center of the hole
        """
        super().__init__()
        
        self.hole_center = hole_center
                
        # load image and get rects
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pipe", "pipe.png")).convert_alpha(), (PIPE_WIDHT, HEIGHT))
        
        if type == PIPE_UPPER:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(midbottom = (WIDTH, self.hole_center - PIPE_HOLE_SIZE/2))
        else:
            self.rect = self.image.get_rect(midtop = (WIDTH, self.hole_center + PIPE_HOLE_SIZE/2))


    def __update_coordinates(self) -> None:
        """Updates the coordinates of the pipe
        """
        self.rect.x -= PIPE_SPEED
        
        if self.rect.x + PIPE_WIDHT < 0:
            self.kill()
            pygame.event.post(pygame.event.Event(HIGHSCORE_NEW_PONIT))
    
    def update(self) -> None:
        """Updates all parameters of the pipe
        """
        self.__update_coordinates()
    