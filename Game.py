import pygame
import os
import random

import Pipe
import Bird

from constants import CAPTION, GREEN, WIDTH, HEIGHT, HIGHSCORE_FONT, RED, LOOSE_FONT, BIRD_HEIGHT, PIPE_LOWER, PIPE_UPPER, PIPE_SPAWN, PIPE_SPAWN_TIMER

class Game:
    def __init__(self):
        self.win = self.__init_window()
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background", "background.png")), (WIDTH, HEIGHT))
        self.highscore = 0


    def __init_window(self):
        """
        Initializes the window for the game
    
        :return: the surface object
        """
        pygame.display.set_caption(CAPTION)
        win = pygame.display.set_mode((WIDTH, HEIGHT))
    
        return win
    
    def start_game(self):
        self.highscore = 0
        
        # set up pipe sprite group and add first pipe
        self.pipes = pygame.sprite.Group()
        hole_center = random.randrange(0 + BIRD_HEIGHT, HEIGHT - BIRD_HEIGHT)
        self.pipes.add(Pipe.Pipe(PIPE_LOWER, hole_center))
        self.pipes.add(Pipe.Pipe(PIPE_UPPER, hole_center))
        
        # set up pipe timer
        pygame.time.set_timer(PIPE_SPAWN, PIPE_SPAWN_TIMER*1000)
        
        # get the player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Bird.Bird())
        
    def stop_game(self):
        # delete objects
        self.pipes = []
        self.player = []
        
        # stop timer
        pygame.time.set_timer(PIPE_SPAWN, 0)

        
    def __draw_background(self):
        """
        draws the background
        
        :return: nothing
        """
        self.win.blit(self.BACKGROUND, (0,0))

    
    def __draw_window(self):
        """
        draws the basic window

        :param highscore: the current highscore    
        :return: nothing
        """
        # draw background
        self.__draw_background()
        
        # draw highscore
        highscore_text = HIGHSCORE_FONT.render("Highscore: " + str(round(self.highscore)), 1, RED)
        self.win.blit(highscore_text, ((10,10)))
        

    def draw_start_screen(self):
        """
        draws the start screen
        
        :return: nothing
        """
        self.__draw_background()
        line1 = LOOSE_FONT.render("Welcome to flappypython V2", 1, GREEN)
        line2 = LOOSE_FONT.render("Press enter to play", 1, GREEN)
        self.win.blit(line1, (round((WIDTH/2) - line1.get_width()/2), round(HEIGHT/2 - line1.get_height()/2)))
        self.win.blit(line2, (round((WIDTH/2) - line2.get_width()/2), round(HEIGHT/2 - line1.get_height()/2) + line1.get_height() + 5))        
        pygame.display.update()

    def draw_lost(self):
        """
        draws the "you lost" screen for 3 seconds
        
        :return: nothing
        """
        self.__draw_background()
        line1 = LOOSE_FONT.render("You loose!! Highscore: " + str(round(self.highscore)), 1, RED)
        line2 = LOOSE_FONT.render("Press enter to play again", 1, RED)
        self.win.blit(line1, (round((WIDTH/2) - line1.get_width()/2), round(HEIGHT/2 - line1.get_height()/2)))
        self.win.blit(line2, (round((WIDTH/2) - line2.get_width()/2), round(HEIGHT/2 - line1.get_height()/2) + line1.get_height() + 5))        
        pygame.display.update()
        
    def spawn_pipe(self):
        """
        adds another pipe
        
        :return: nothing
        """
        hole_center = random.randrange(0 + BIRD_HEIGHT, HEIGHT - BIRD_HEIGHT)
        self.pipes.add(Pipe.Pipe(PIPE_LOWER, hole_center))
        self.pipes.add(Pipe.Pipe(PIPE_UPPER, hole_center))
        
    def collision_sprite(self):
        """
        checks if the sprites collide
        
        :return: Boolean if sprites collide or not
        """
        if pygame.sprite.spritecollide(self.player.sprite,self.pipes,False):
            return True
        else: 
            return False
        
    def update(self, keys_pressed):
        """
        updates all game entities
        
        :param keys_pressed: arrays of pressed keys
        :return: nothing
        """
        self.player.update(keys_pressed)
        self.pipes.update()
        
    def draw_game(self):
        """
        draws all game entities
        
        :return: nothing
        """
        self.__draw_window()
        self.pipes.draw(self.win)
        self.player.draw(self.win)
        pygame.display.update()
