import pygame
import os
from constants import *
from gamedata import *
from interface import *


def main():
    
    pygame.init()

    screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE + 200, MAP_HEIGHT * TILE_SIZE))
    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join('images', 'map.png'))
    background = pygame.transform.scale(background, (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))


    player_hero = Hero(1, MAP_HEIGHT-2, 'hero.png')  
    enemy_hero = Hero(MAP_WIDTH-2, 1, 'enemy.png')  
    cat_house = House(0, MAP_HEIGHT -3, 'CatHouse.png') 

    win_dialog_frame = pygame.Rect(MAP_WIDTH * TILE_SIZE / 2 - 130, (MAP_HEIGHT * TILE_SIZE) / 2 - 90, 260, 180)


    font = pygame.font.Font(None, 50)
    win_text = font.render('You win!', True, (0, 0, 0))
    win_text_position = win_text.get_rect(center=(win_dialog_frame.width//2, win_dialog_frame.height//2 - 40))  # reduce Y value to move text up
    screen.blit(win_text, (win_dialog_frame.x + win_text_position.x, win_dialog_frame.y + win_text_position.y))
    ok_button = Button(MAP_WIDTH * TILE_SIZE / 2 - 40, (MAP_HEIGHT * TILE_SIZE) / 2 + 10, 80, 40, LIGHT_BLUE, 'OK')
    show_win_dialog = False

    moves = MovesCounter(3)
    end_turn_button = Button(MAP_WIDTH * TILE_SIZE + 60, MAP_HEIGHT * TILE_SIZE - 50, 80, 40, LIGHT_BLUE, 'End Turn')



    # def draw_grid(screen):
    #     for x in range(0, MAP_WIDTH * TILE_SIZE, TILE_SIZE):
    #         for y in range(0, MAP_HEIGHT * TILE_SIZE, TILE_SIZE):
    #             pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 1)

    # def draw_tile_numbers(screen):
    #     font = pygame.font.Font(None, 24)
    #     number = 1
    #     for y in range(MAP_HEIGHT-1, -1, -1):  # start from the bottom
    #         for x in range(MAP_WIDTH):
    #             text = font.render(str(number), True, (0, 0, 0))
    #             screen.blit(text, (x * TILE_SIZE + TILE_SIZE / 2 - text.get_width() / 2, y * TILE_SIZE + TILE_SIZE / 2 - text.get_height() / 2))
    #             number += 1


    target_x, target_y = player_hero.x, enemy_hero.y
    resources = Resources()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    moves.moves = 3
                    player_hero.reset_target()
                if event.key == pygame.K_LEFT:
                    player_hero.set_target(player_hero.x - 1, player_hero.y)
                elif event.key == pygame.K_RIGHT:
                    player_hero.set_target(player_hero.x + 1, player_hero.y)
                elif event.key == pygame.K_UP:
                    player_hero.set_target(player_hero.x, player_hero.y - 1)
                elif event.key == pygame.K_DOWN:
                    player_hero.set_target(player_hero.x, player_hero.y + 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if show_win_dialog and ok_button.isOver(pos):
                    running = False
                if end_turn_button.isOver(pos):
                    moves.moves = 3
                    player_hero.reset_target()
                else:
                    target_x, target_y = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
                    player_hero.set_target(target_x, target_y)

        player_hero.update(moves)

        #print(f"Player coordinates: ({map[player_hero.y][player_hero.x]})")
        #draw_grid(screen)
        #draw_tile_numbers(screen)
        
        
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        
        cat_house.draw(screen)
        
        player_hero.draw(screen)
        enemy_hero.draw(screen)
        
        Resources.draw_resources(screen, resources)
        moves.draw(screen, MAP_WIDTH * TILE_SIZE + 60, MAP_HEIGHT * TILE_SIZE - 100)
        end_turn_button.draw(screen)

        # check if the hero has reached the enemy
        if (player_hero.x, player_hero.y) == (enemy_hero.x, enemy_hero.y):
            show_win_dialog = True

        if show_win_dialog:
            # draw the win dialog frame
            pygame.draw.rect(screen, LIGHT_BLUE, win_dialog_frame)
            pygame.draw.rect(screen, BLACK, win_dialog_frame, 2)

            # draw the win text
            screen.blit(win_text, (win_dialog_frame.x + win_text_position.x, win_dialog_frame.y + win_text_position.y))

            # draw the OK button
            ok_button.draw(screen)
            pygame.draw.rect(screen, BLACK, ok_button.rect, 2)



        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()