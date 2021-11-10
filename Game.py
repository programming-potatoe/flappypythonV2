import pygame
import os
import random
from typing import List

from pygame.constants import K_ESCAPE, K_RETURN

import Pipe
import Bird

from constants import CAPTION, FPS, GAME_LOST, GREEN, HIGHSCORE_NEW_PONIT, WIDTH, HEIGHT, HIGHSCORE_FONT, RED, LOOSE_FONT, BIRD_HEIGHT, PIPE_LOWER, PIPE_UPPER, PIPE_SPAWN, PIPE_SPAWN_TIMER, Gamemodes

class Game:
    """The class that contains all game logic
    
    Attributes:
        win: the pygame win object of the game
        BACKGROUND: the image of the background
        highscore: the current highscore of the game
        clock: the pygame clock object
        gamemode: the current gamemode of the game
    """
    def __init__(self) -> None:
        """Init function of the game class
        """
        self.win = self.__init_window()
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background", "background.png")), (WIDTH, HEIGHT))
        self.highscore = 0
        self.gamemode = Gamemodes.startscreen
        self.clock = pygame.time.Clock()


    def __init_window(self) -> pygame.Surface:
        """Initializes the window for the game
        
        Returns:
            the surface object
        """
        pygame.display.set_caption(CAPTION)
        win = pygame.display.set_mode((WIDTH, HEIGHT))
    
        return win
    
    def __start_game(self) -> None:
        """Sets up the game objects
        """
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
        
    def __stop_game(self) -> None:
        """Removes all game objects and timers
        """
        # delete objects
        self.pipes = []
        self.player = []
        
        # stop timer
        pygame.time.set_timer(PIPE_SPAWN, 0)

        
    def __draw_background(self) -> None:
        """Draws the background
        """
        self.win.blit(self.BACKGROUND, (0,0))

    
    def __draw_window(self) -> None:
        """Draws the basic window
        """
        # draw background
        self.__draw_background()
        
        # draw highscore
        highscore_text = HIGHSCORE_FONT.render("Highscore: " + str(round(self.highscore)), 1, RED)
        self.win.blit(highscore_text, ((10,10)))

    def __draw_game(self) -> None:
        """Draws all game entities
        """
        self.__draw_window()
        self.pipes.draw(self.win)
        self.player.draw(self.win)
        pygame.display.update()
  

    def __draw_startscreen(self) -> None:
        """Draws the startscreen
        """
        self.__draw_background()
        line1 = LOOSE_FONT.render("Welcome to FlappyPython V2", 1, GREEN)
        line2 = LOOSE_FONT.render("Press enter to play", 1, GREEN)
        self.win.blit(line1, (round((WIDTH/2) - line1.get_width()/2), round(HEIGHT/2 - line1.get_height()/2)))
        self.win.blit(line2, (round((WIDTH/2) - line2.get_width()/2), round(HEIGHT/2 - line1.get_height()/2) + line1.get_height() + 5))        
        pygame.display.update()

    def __draw_lostscreen(self) -> None:
        """Draws the "you lost" screen for 3 seconds
        """
        self.__draw_background()
        line1 = LOOSE_FONT.render("You loose!! Highscore: " + str(round(self.highscore)), 1, RED)
        line2 = LOOSE_FONT.render("Press enter to play again", 1, RED)
        self.win.blit(line1, (round((WIDTH/2) - line1.get_width()/2), round(HEIGHT/2 - line1.get_height()/2)))
        self.win.blit(line2, (round((WIDTH/2) - line2.get_width()/2), round(HEIGHT/2 - line1.get_height()/2) + line1.get_height() + 5))        
        pygame.display.update()
        
    def __spawn_pipe(self) -> None:
        """Adds another pipe to the pipe list
        """
        hole_center = random.randrange(0 + BIRD_HEIGHT, HEIGHT - BIRD_HEIGHT)
        self.pipes.add(Pipe.Pipe(PIPE_LOWER, hole_center))
        self.pipes.add(Pipe.Pipe(PIPE_UPPER, hole_center))
        
    def __collision_sprite(self) -> bool:
        """Checks if the sprites of player bird and pipes collide
        
        Returns:
            if player and pipes collide or not
        """
        if pygame.sprite.spritecollide(self.player.sprite,self.pipes,False):
            return True
        else: 
            return False
        
    def __handle_ingame_events(self, events: List[pygame.event.Event]) -> None:
        """Handles all events that happen in game
        
        Args:
            events: list of all events
        """
        for event in events:
            if event.type == HIGHSCORE_NEW_PONIT:
                self.highscore += 0.5
            if event.type == PIPE_SPAWN:
                self.__spawn_pipe()

    def __update(self, keys_pressed: List[int]) -> None:
        """Updates all game entities
        
        Args:
            keys_pressed: arrays of pressed keys
       """
        self.player.update(keys_pressed)
        self.pipes.update()
    
    def set_gamemode(self, events: List[pygame.event.Event], keys_pressed: List[int]) -> None:
        """Sets gamemode based on events and pressed keys
        
        Args:
            events: list of all events
            keys_pressed: list of all pressed keys
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
        """Does stuff for the startscreen
        """
        self.__draw_startscreen()
    
    def gamemode_running(self) -> None:
        """Executes the gamemode running
        """
        self.__start_game() 
                        
        while self.gamemode == Gamemodes.running:

            self.clock.tick(FPS)

            # get all events
            events = pygame.event.get()

            # get all keys pressend
            keys_pressed = pygame.key.get_pressed()

            # handle ingame events
            self.__handle_ingame_events(events)

            # set gamemode based on events
            self.set_gamemode(events, keys_pressed)

            # react to gamestop
            if self.gamemode != Gamemodes.running:
                self.__stop_game()
                break                

            # update all things
            self.__update(keys_pressed)

            # draw game
            self.__draw_game()
                        
            # check for collisions
            if self.__collision_sprite():
                self.gamemode = Gamemodes.lostscreen

            if self.gamemode != Gamemodes.running:
                self.__stop_game()
                break
    
    def gamemode_lostscreen(self) -> None:
        """Executes the gamemode lostscreen
        """
        self.__draw_lostscreen()