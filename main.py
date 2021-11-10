import pygame
from pygame.constants import K_ESCAPE, K_RETURN
pygame.font.init()
pygame.mixer.init()
pygame.init()

import Game

from constants import GAME_LOST, FPS, HIGHSCORE_NEW_PONIT, PIPE_SPAWN, Gamemodes

def window_close_pressed() -> None:
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

def main() -> None:
    """
    main loop of the game
    
    :return: nothing
    """
    run = True

    # create the game class
    game = Game.Game()

    # main game loop
    while run:
                                
        # set the game mode
        game.set_gamemode(pygame.event.get(), pygame.key.get_pressed())
        
        # execute the different gamemodes
        if game.gamemode == Gamemodes.startscreen:
            game.gamemode_startscreen()
        
        elif game.gamemode == Gamemodes.running:
            game.gamemode_running()
                
        elif game.gamemode == Gamemodes.lostscreen:
            game.gamemode_lostscreen()
            
        elif game.gamemode == Gamemodes.exit:
            run = False
            pygame.quit()
        
        else:
            run = False
            pygame.quit()
    
# run main only if this file is run directly
if __name__ == "__main__":
    main()