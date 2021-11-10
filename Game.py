import pygame
import os
import random
from typing import List

from pygame.constants import K_ESCAPE, K_RETURN

import Pipe
import Bird

from constants import CAPTION, FPS, GAME_LOST, GREEN, HIGHSCORE_NEW_PONIT, WIDTH, HEIGHT, HIGHSCORE_FONT, RED, LOOSE_FONT, BIRD_HEIGHT, PIPE_LOWER, PIPE_UPPER, PIPE_SPAWN, PIPE_SPAWN_TIMER, Gamemodes

class Game:
    def __init__(self) -> None:
        self.win = self.__init_window()
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background", "background.png")), (WIDTH, HEIGHT))
        self.highscore = 0
        self.gamemode = Gamemodes.startscreen
        self.clock = pygame.time.Clock()


    def __init_window(self) -> pygame.Surface:
        """
        Initializes the window for the game
    
        :return: the surface object
        """
        pygame.display.set_caption(CAPTION)
        win = pygame.display.set_mode((WIDTH, HEIGHT))
    
        return win
    
    def start_game(self) -> None:
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
        
    def stop_game(self) -> None:
        # delete objects
        self.pipes = []
        self.player = []
        
        # stop timer
        pygame.time.set_timer(PIPE_SPAWN, 0)

        
    def __draw_background(self) -> None:
        """
        draws the background
        
        :return: nothing
        """
        self.win.blit(self.BACKGROUND, (0,0))

    
    def __draw_window(self) -> None:
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
        

    def draw_start_screen(self) -> None:
        """
        draws the start screen
        
        :return: nothing
        """
        self.__draw_background()
        line1 = LOOSE_FONT.render("Welcome to FlappyPython V2", 1, GREEN)
        line2 = LOOSE_FONT.render("Press enter to play", 1, GREEN)
        self.win.blit(line1, (round((WIDTH/2) - line1.get_width()/2), round(HEIGHT/2 - line1.get_height()/2)))
        self.win.blit(line2, (round((WIDTH/2) - line2.get_width()/2), round(HEIGHT/2 - line1.get_height()/2) + line1.get_height() + 5))        
        pygame.display.update()

    def draw_lost(self) -> None:
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
        
    def spawn_pipe(self) -> None:
        """
        adds another pipe
        
        :return: nothing
        """
        hole_center = random.randrange(0 + BIRD_HEIGHT, HEIGHT - BIRD_HEIGHT)
        self.pipes.add(Pipe.Pipe(PIPE_LOWER, hole_center))
        self.pipes.add(Pipe.Pipe(PIPE_UPPER, hole_center))
        
    def collision_sprite(self) -> None:
        """
        checks if the sprites collide
        
        :return: Boolean if sprites collide or not
        """
        if pygame.sprite.spritecollide(self.player.sprite,self.pipes,False):
            return True
        else: 
            return False
        
    def handle_ingame_events(self, events: List[pygame.event.Event]) -> None:
        """
        handles all events that happen in game
        
        :param events: list of all events
        :return: nothing
        """
        for event in events:
            if event.type == HIGHSCORE_NEW_PONIT:
                self.highscore += 0.5
            if event.type == PIPE_SPAWN:
                self.spawn_pipe()
    
    def set_gamemode(self, events: List[pygame.event.Event], keys_pressed: List[int]) -> None:
        """
        sets gamemode based on events and pressed keys
        
        :param events: list of all events
        :param keys_pressed: list of all pressed keys
        :return: nothing
        """        
        for event in events:
            if event.type == pygame.QUIT:
                self.gamemode = Gamemodes.exit
            if event.type == GAME_LOST:
                self.gamemode = Gamemodes.lostscreen
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                self.gamemode = Gamemodes.exit
        
        if keys_pressed[K_ESCAPE]:
            self.gamemode = Gamemodes.exit
        elif keys_pressed[K_RETURN] and self.gamemode in [Gamemodes.startscreen, Gamemodes.lostscreen]:
            self.gamemode = Gamemodes.running


    
    def gamemode_startscreen(self) -> None:
        """does stuff for the startscreen
        
        Args:
            self: this object
        
        Returns:
            nothing
        """
        self.draw_start_screen()
    
    def gamemode_running(self) -> None:
        """
        test_function does blah blah blah
        
        :param p1: describe about parameter p1
        :return: describe what it returns
        """
        self.start_game() 
                        
        while self.gamemode == Gamemodes.running:

            self.clock.tick(FPS)

            # get all events
            events = pygame.event.get()

            # get all keys pressend
            keys_pressed = pygame.key.get_pressed()

            # handle ingame events
            self.handle_ingame_events(events)

            # set gamemode based on events
            self.set_gamemode(events, keys_pressed)

            # react to gamestop
            if self.gamemode != Gamemodes.running:
                self.stop_game()
                break                

            # update all things
            self.update(keys_pressed)

            # draw game
            self.draw_game()
                        
            # check for collisions
            if self.collision_sprite():
                self.gamemode = Gamemodes.lostscreen

            if self.gamemode != Gamemodes.running:
                self.stop_game()
                break
    
    def gamemode_lostscreen(self) -> None:
        """
        test_function does blah blah blah
        
        :return: nothing
        """
        self.draw_lost()
        
    def update(self, keys_pressed: List[int]) -> None:
        """
        updates all game entities
        
        :param keys_pressed: arrays of pressed keys
        :return: nothing
        """
        self.player.update(keys_pressed)
        self.pipes.update()
        
    def draw_game(self) -> None:
        """
        draws all game entities
        
        :return: nothing
        """
        self.__draw_window()
        self.pipes.draw(self.win)
        self.player.draw(self.win)
        pygame.display.update()
