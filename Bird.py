import pygame
import os

from constants import BIRD_HEIGHT, BIRD_WIDTH, BIRD_SPAWN, GAME_LOST, HEIGHT, BIRD_INITIAL_STEP_SIZE, BIRD_MAX_ROTATION_DOWN, BIRD_MAX_ROTATION_UP

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # image variable of the bird
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bird", "bird.png")).convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))
        self.angle = 0
        
        # images for flying
        fly_1 = self.image
        fly_2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bird", "bird2.png")).convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))
        self.fly = [fly_1, fly_2]
        self.animation_index = 0
        
        # image for glyding
        self.glide = self.image
        
        # get the rect of the bird
        self.rect = self.image.get_rect(center = BIRD_SPAWN)
        
        # set initial gravity
        self.gravity = 0
        self.step_size = 5
        
    def __handle_user_input(self, keys_pressed):
        """
        checks for the user input and adjusts gravity and step_size accordingly

        :param keys_pressed: array with all pressed keys
        :return: nothing
        """
        # if key is pressed negative gravity, else positive gravity
        if keys_pressed[pygame.K_SPACE]:
            if self.gravity >= 0:
                self.gravity = -BIRD_INITIAL_STEP_SIZE
                self.step_size = BIRD_INITIAL_STEP_SIZE
            else:
                self.gravity -= self.step_size
                self.step_size += 1
        else:
            if self.gravity <= 0:
                self.gravity = BIRD_INITIAL_STEP_SIZE
                self.step_size = BIRD_INITIAL_STEP_SIZE
            else:
                self.gravity += self.step_size
                self.step_size += 1

    def __update_coordinates(self):
        """
        updates the coordinates of the bird using the gravity
        
        :return: nothing
        """
        # apply gravity
        self.rect.y += self.gravity
        
        # respect lower bound => game is lost
        if self.rect.y + BIRD_HEIGHT > HEIGHT:
            self.rect.y = HEIGHT - BIRD_HEIGHT
            pygame.event.post(pygame.event.Event(GAME_LOST))
            
        # respect upper bound
        if self.rect.y < 0:
            self.rect.y = 0
            
    def __update_image(self):
        """
        updates the image of the bird (rotation and animation)
        
        :return: nothing
        """
        if self.gravity > 0:
            # bird is going down => only gliding and rotation downwards
            self.image = self.glide
            self.angle -= 5
            
            # only rotate until threshold
            if self.angle <= -BIRD_MAX_ROTATION_DOWN:
                self.angle = -BIRD_MAX_ROTATION_DOWN

        else:
            # bird is going up => flying animation and rotation upwards
            if self.animation_index == 0:
                self.animation_index = 1
            else:
                self.animation_index = 0
            
            self.image = self.fly[self.animation_index]    
            
            self.angle += 10
            
            # only rotate until threshold
            if self.angle >= BIRD_MAX_ROTATION_UP:
                self.angle = BIRD_MAX_ROTATION_UP
        
        # rotate the image
        self.image = pygame.transform.rotate(self.image, self.angle)

    
    def update(self, keys_pressed):
        """
        updates all properties of the bird
        
        :param keys_pressed: array of all keys pressed
        :return: nothing
        """
        self.__handle_user_input(keys_pressed)
        self.__update_coordinates()
        self.__update_image()