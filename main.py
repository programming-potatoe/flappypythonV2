import pygame
from pygame.constants import K_ESCAPE, K_RETURN
pygame.font.init()
pygame.mixer.init()
pygame.init()

import Game

from constants import GAME_LOST, FPS, HIGHSCORE_NEW_PONIT, PIPE_SPAWN, Gamemodes

def window_close_pressed():
    """
    checks if the window close button was pressed
    
    :return: boolean, true if window close button was pressed
    """
    # get all events
    events = pygame.event.get()

    # check all events
    for event in events:
        if event.type == pygame.QUIT:
            return True
        
    return False

def main():
    """
    main loop of the game
    
    :return: nothing
    """
    run = True
    
    gamemode = Gamemodes.start_screen

    # set up the clock
    clock = pygame.time.Clock()

    # create the game class
    game = Game.Game()

    # main game loop
    while run:
        
        # get all pressed keys
        pygame.event.pump()
        keys_pressed = pygame.key.get_pressed()
                                
        # set the game mode
        if keys_pressed[K_ESCAPE]:
            gamemode = Gamemodes.exit
        elif keys_pressed[K_RETURN] and gamemode in [Gamemodes.start_screen, Gamemodes.lost_screen]:
            gamemode = Gamemodes.running
        
        # execute the different gamemodes
        if gamemode == Gamemodes.start_screen:
            game.draw_start_screen()

            # get all events
            events = pygame.event.get()

            # check all events
            for event in events:
                if event.type == pygame.QUIT:
                    gamemode = Gamemodes.exit
        
        elif gamemode == Gamemodes.running:
            game.start_game() 
                                    
            while gamemode == Gamemodes.running:
                clock.tick(FPS)
                
                # get all events
                events = pygame.event.get()

                # get all keys pressend
                keys_pressed = pygame.key.get_pressed()
                
                # check all events
                for event in events:
                    if event.type == pygame.QUIT:
                        gamemode = Gamemodes.exit
                    if event.type == HIGHSCORE_NEW_PONIT:
                        game.highscore += 0.5
                    if event.type == PIPE_SPAWN:
                        game.spawn_pipe()
                    if event.type == GAME_LOST:
                        gamemode = Gamemodes.lost_screen
                    if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                        gamemode = Gamemodes.exit
                        
                if gamemode != Gamemodes.running:
                    game.stop_game()
                    break                
                
                # update all things
                game.update(keys_pressed)

                # draw game
                game.draw_game()
                                
                # check for collisions
                if game.collision_sprite():
                    gamemode = Gamemodes.lost_screen
                
                if gamemode != Gamemodes.running:
                    game.stop_game()
                    break
                
        elif gamemode == Gamemodes.lost_screen:
            game.draw_lost()
            
            

        elif gamemode == Gamemodes.exit:
            run = False
            pygame.quit()
        
        else:
            run = False
            pygame.quit()
    
# run main only if this file is run directly
if __name__ == "__main__":
    main()