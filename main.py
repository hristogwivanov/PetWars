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



    def draw_map_objects(event_map):

        for y, row in enumerate(event_map):
            for x, item in enumerate(row):
                draw_dictionary = {
                    11: lambda: drawCatHouse(x, y, screen),
                    12: lambda: drawDogHouse(x, y, screen),
                    21: lambda: drawGold(x, y, screen),
                    22: lambda: drawGold(x, y, screen),
                    23: lambda: drawGold(x, y, screen),
                    31: lambda: drawMilk(x, y, screen),
                    32: lambda: drawMilk(x, y, screen),
                    41: lambda: drawFish(x, y, screen),
                    51: lambda: drawDoge(x, y, screen),
                    52: lambda: drawDoge(x, y, screen),
                    53: lambda: drawDoge(x, y, screen),
                    61: lambda: drawBones(x, y, screen),
                    62: lambda: drawBones(x, y, screen),
                    71: lambda: drawMeat(x, y, screen),
                    101: lambda: drawMilkFarm(x, y, screen),
                    102: lambda: drawFishPound(x, y, screen),
                    151: lambda: drawBoneYard(x, y, screen),
                    152: lambda: drawPigFarm(x, y, screen),
                    211: lambda: drawMouse(x, y, screen),
                    212: lambda: drawStreetCat(x, y, screen),
                    213: lambda: drawPersianCat(x, y, screen),
                    214: lambda: drawSphynxCat(x, y, screen),
                    221: lambda: drawFlippedMouse(x, y, screen),
                    222: lambda: drawPugDog(x, y, screen),
                    223: lambda: drawMalinoisDog(x, y, screen),
                    224: lambda: drawShibaInuDog(x, y, screen),
                    230: lambda: drawDragon(x, y, screen),
                }
                if item in draw_dictionary:
                    draw_dictionary[item]()



    


    player_hero = Hero(1, MAP_HEIGHT-2, 'hero.png')  
    enemy_hero = Hero(MAP_WIDTH-2, 1, 'enemy.png')  

    #####LEGACT CODE - The resources were presented as instances of class, now they are just on the event map#####

    # cat_house = House(0, MAP_HEIGHT -3, 'CatHouse.png') 
    # dog_house = House(MAP_WIDTH-2.7, 0, 'DogHouse.png') 
    # resources_on_map=[]
    # milk1 = Resource(0, 5, 'milk', 10)
    # milk2 = Resource(3, 0, 'milk', 20)
    # meowcoins1 = Resource(0, 4, 'meowcoins', 10000)
    # meowcoins2 = Resource(3, 1, 'meowcoins', 20000)
    # meowcoins3 = Resource(7, 5, 'meowcoins', 100000)
    # fish1 = Resource(1, 5, 'fish', 10)
    # dogecoins1 = Resource(13, 5, 'dogecoins', 10000)
    # dogecoins2 = Resource(10, 8, 'dogecoins', 20000)
    # dogecoins3 = Resource(7, 6, 'dogecoins', 20000)
    # bones1 = Resource(13, 4, 'bones', 10)
    # bones2 = Resource(10, 9, 'bones', 20)
    # meat1 = Resource(12, 4, 'meat', 10)
    # resources_on_map.extend([milk1, milk2, meowcoins1, meowcoins2, meowcoins3, fish1, dogecoins1, dogecoins2, dogecoins3, bones1, bones2, meat1])

    # milkfarm = Farm(5, 9, 'milk')

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


    resources = Resources()



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    end_of_turn(resources, moves, player_hero)
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
                    end_of_turn(resources, moves, player_hero)
                else:
                    target_x, target_y = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
                    player_hero.set_target(target_x, target_y)

        player_hero.update(moves)

        #print(f"Player coordinates: ({map[player_hero.y][player_hero.x]})")
        #draw_grid(screen)
        #draw_tile_numbers(screen)
        
        
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        
        # cat_house.draw(screen)
        # dog_house.draw(screen)
        
        draw_map_objects(event_map)
        player_hero.draw(screen)
        enemy_hero.draw(screen)


        # for resource in resources_on_map:
        #     resource.draw(screen)

        # milkfarm.draw(screen)

        #milk1.draw(screen)
        #milk2.draw(screen)
        
        Resources.draw_resources(screen, resources)
        draw_date(screen)
        moves.draw(screen, MAP_WIDTH * TILE_SIZE + 60, MAP_HEIGHT * TILE_SIZE - 100)
        end_turn_button.draw(screen)

        # check if the hero has reached the enemy
        if (player_hero.x, player_hero.y) == (enemy_hero.x, enemy_hero.y):
            show_win_dialog = True



        #check if there is event

        event_dictionary = {
            # 11: ownTown,
            # 12: enemyTown,
            21: lambda: getGold(10000, resources),
            22: lambda: getGold(20000, resources),
            23: lambda: getGold(100000, resources),
            31: lambda: getMilk(10, resources),
            32: lambda: getMilk(20, resources),
            41: lambda: getFish(10, resources),
            51: lambda: getDoge(10000, resources),
            52: lambda: getDoge(20000, resources),
            53: lambda: getDoge(100000, resources),
            61: lambda: getBones(10, resources),
            62: lambda: getBones(20, resources),
            71: lambda: getMeat(10, resources),
            101: lambda: visitMilkFarm(resources),
            102: lambda: visitFishPound(resources),
            151: lambda: visitBoneYard(resources),
            152: lambda: visitPigFarm(resources),
            # 211: neutral11,
            # 212: neutral12,
            # 213: neutral13,
            # 214: neutral14,
            # 221: neutral21,
            # 222: neutral22,
            # 223: neutral23,
            # 224: neutral24,
            # 230: neutral30
        }

        if event_map[player_hero.y][player_hero.x]>20:
            # print(event_map[player_hero.y][player_hero.x])
            # print(player_hero.x)
            # print(player_hero.y)
            if event_map[player_hero.y][player_hero.x] in event_dictionary:
                event_dictionary[event_map[player_hero.y][player_hero.x]]()
                if event_map[player_hero.y][player_hero.x] >=20 and event_map[player_hero.y][player_hero.x] <=100: 
                    event_map[player_hero.y][player_hero.x] = 0



        # check if hero got milk
        # for item in resources_on_map:
        #     if (player_hero.x, player_hero.y) == (item.x, item.y):
        #         match item.type:
        #             case 'meowcoins':
        #                 resources.meowcoins+=item.quantity
        #             case 'milk':
        #                 resources.milk+=item.quantity
        #             case 'fish':
        #                 resources.fish=item.quantity
        #             case _:
        #                 pass
        #         resources_on_map = [resource for resource in resources_on_map if not (resource.x == player_hero.x and resource.y == player_hero.y)]

        # if (player_hero.x, player_hero.y) == (milk1.x, milk1.y):
        #     if milk1 in resources_on_map: 
        #         resources.milk+=milk1.quantity
        #         resources_on_map = [resource for resource in resources_on_map if not (resource.x == player_hero.x and resource.y == player_hero.y)]
        # if (player_hero.x, player_hero.y) == (milk2.x, milk2.y):
        #     if milk2 in resources_on_map: 
        #         resources.milk+=milk2.quantity
        #         resources_on_map = [resource for resource in resources_on_map if not (resource.x == player_hero.x and resource.y == player_hero.y)]


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