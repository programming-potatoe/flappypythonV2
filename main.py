import random
import pygame
pygame.font.init()
pygame.mixer.init()
pygame.init()

import os
import Bird
import Pipe

from constants import HIGHSCORE_FONT, LOOSE_FONT, WIDTH, HEIGHT, CAPTION, FPS, GAME_LOST, HIGHSCORE_NEW_PONIT, RED, PIPE_SPAWN, PIPE_SPAWN_TIMER, PIPE_UPPER, PIPE_LOWER, BIRD_HEIGHT

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background", "background.png")), (WIDTH, HEIGHT))

def init_window():
    """
    Initializes the window for the game
    
    :return: the surface object
    """
    pygame.display.set_caption(CAPTION)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    
    return win

def draw_window(win, highscore):
    """
    draws the basic window
    
    :param win: the window to draw on
    :param highscore: the current highscore    
    :return: nothing
    """
    # draw background
    win.blit(BACKGROUND, (0,0))
    
    # draw highscore
    highscore_text = HIGHSCORE_FONT.render("Highscore: " + str(round(highscore)), 1, RED)
    win.blit(highscore_text, ((10,10)))
    
    pygame.display.update()

def draw_lost(win, highscore):
    """
    draws the "you lost" screen for 3 seconds
    
    :param win: the window to draw on
    :param highscore: the current highscore
    :return: nothing
    """
    loose_text = LOOSE_FONT.render("You loose!! Highscore: " + str(round(highscore)), 1, RED)
    win.blit(loose_text, (round((WIDTH/2) - loose_text.get_width()/2), round(HEIGHT/2 - loose_text.get_height()/2)))
    pygame.display.update()
    pygame.time.delay(3000)
    
    

def collision_sprite(player, pipes):
    """
    checks if the sprites collide
    
    :param player: the player sprite
    :param pipes: the sprite group of all sprites
    :return: Boolean if sprites collide or not
    """
    if pygame.sprite.spritecollide(player.sprite,pipes,False):
        return True
    else: 
        return False

def main():
    """
    main loop of the game
    
    :return: nothing
    """
    # clear events in case something got stuck from last loop
    pygame.event.clear()

    # set up the clock
    clock = pygame.time.Clock()
    
    # set up highscore
    highscore = 0
        
    run = True
    
    # set up the window
    win = init_window()
    
    # set up pipe sprite group and add first pipe
    pipes = pygame.sprite.Group()
    hole_center = random.randrange(0 + BIRD_HEIGHT, HEIGHT - BIRD_HEIGHT)
    pipes.add(Pipe.Pipe(PIPE_LOWER, hole_center))
    pipes.add(Pipe.Pipe(PIPE_UPPER, hole_center))
    
    # set up pipe timer
    pygame.time.set_timer(PIPE_SPAWN, PIPE_SPAWN_TIMER*1000)
    
    # get the player
    player = pygame.sprite.GroupSingle()
    player.add(Bird.Bird())
    
    # start game loop
    while run:
        clock.tick(FPS)

        # iterate through all events
        events = pygame.event.get()
        
        # check all events
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == HIGHSCORE_NEW_PONIT:
                highscore += 0.5
            if event.type == GAME_LOST:
                draw_lost(win, highscore)
                run = False
            if event.type == PIPE_SPAWN:
                hole_center = random.randrange(0 + BIRD_HEIGHT, HEIGHT - BIRD_HEIGHT)
                pipes.add(Pipe.Pipe(PIPE_LOWER, hole_center))
                pipes.add(Pipe.Pipe(PIPE_UPPER, hole_center))
                
        if run == False:
            exit
        
        # update objects
        player.update()
        pipes.update()
        
        # check for collisions
        if collision_sprite(player, pipes):
            pygame.event.post(pygame.event.Event(GAME_LOST))
        
        # draw window
        draw_window(win, highscore)
        pipes.draw(win)
        player.draw(win)
        
        
        pygame.display.update()

    main()

# run main only if this file is run directly
if __name__ == "__main__":
    main()