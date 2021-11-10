import pygame
from pygame.constants import K_ESCAPE, K_RETURN
pygame.font.init()
pygame.mixer.init()
pygame.init()

import Game

from constants import GAME_LOST, FPS, HIGHSCORE_NEW_PONIT, PIPE_SPAWN, Gamemodes

def main() -> None:
    """Main loop of the game
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