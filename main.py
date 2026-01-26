import pygame
import os
import constants
from constants import *
from gamedata import *
from gamedata import Cat_Hero
from interface import *
from pathfinding import dijkstra_visual


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


    player_hero = Cat_Hero(1, MAP_HEIGHT-2, 'hero.png')  
    enemy_hero = Dog_Hero(MAP_WIDTH-2, 1, 'enemy.png')  
    player_hero.streetcats += 10

    resources = Resources()

    # Dijkstra visualization state
    dijkstra_generator = None
    dijkstra_state = None
    dijkstra_last_step_time = 0

    def draw_dijkstra_visualization(state):
        """Draw the current state of Dijkstra visualization."""
        if state is None:
            return
        
        # Create semi-transparent surface for overlays
        overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Draw visited nodes (orange)
        if state.get('visited'):
            overlay.fill(COLOR_VISITED)
            for (x, y) in state['visited']:
                screen.blit(overlay, (x * TILE_SIZE, y * TILE_SIZE))
        
        # Draw frontier nodes (yellow)
        if state.get('frontier'):
            overlay.fill(COLOR_FRONTIER)
            for (x, y) in state['frontier']:
                screen.blit(overlay, (x * TILE_SIZE, y * TILE_SIZE))
        
        # Draw current node (red)
        if state.get('current'):
            overlay.fill(COLOR_CURRENT)
            x, y = state['current']
            screen.blit(overlay, (x * TILE_SIZE, y * TILE_SIZE))
        
        # Draw final path (blue)
        if state.get('path'):
            overlay.fill(COLOR_PATH)
            for (x, y) in state['path']:
                screen.blit(overlay, (x * TILE_SIZE, y * TILE_SIZE))

    def draw_demo_mode_indicator():
        """Draw indicator showing demo mode status."""
        font = pygame.font.Font(None, 24)
        mode_text = "DEMO MODE: ON" if constants.DEMO_MODE else "DEMO MODE: OFF"
        color = (0, 150, 0) if constants.DEMO_MODE else (150, 0, 0)
        text = font.render(mode_text, True, color)
        screen.blit(text, (MAP_WIDTH * TILE_SIZE + 20, 140))
        hint_text = font.render("Press D to toggle", True, (100, 100, 100))
        screen.blit(hint_text, (MAP_WIDTH * TILE_SIZE + 20, 160))

    win_dialog_frame = pygame.Rect(MAP_WIDTH * TILE_SIZE / 2 - 130, (MAP_HEIGHT * TILE_SIZE) / 2 - 90, 260, 180)


    font = pygame.font.Font(None, 50)
    win_text = font.render('You win!', True, (0, 0, 0))
    win_text_position = win_text.get_rect(center=(win_dialog_frame.width//2, win_dialog_frame.height//2 - 40))  
    screen.blit(win_text, (win_dialog_frame.x + win_text_position.x, win_dialog_frame.y + win_text_position.y))
    ok_button = Button(MAP_WIDTH * TILE_SIZE / 2 - 40, (MAP_HEIGHT * TILE_SIZE) / 2 + 10, 80, 40, LIGHT_BLUE, 'OK')
    show_win_dialog = False

    moves = MovesCounter(3)
    end_turn_button = Button(MAP_WIDTH * TILE_SIZE + 60, MAP_HEIGHT * TILE_SIZE - 50, 80, 40, LIGHT_BLUE, 'End Turn')


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    end_of_turn(resources, moves, player_hero, enemy_hero, event_dictionary)
                elif event.key == pygame.K_d:
                    # Toggle demo mode
                    constants.DEMO_MODE = not constants.DEMO_MODE
                    print(f"Demo mode: {'ON' if constants.DEMO_MODE else 'OFF'}")
                    # Clear any running visualization
                    dijkstra_generator = None
                    dijkstra_state = None
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
                    end_of_turn(resources, moves, player_hero, enemy_hero, event_dictionary)
                else:
                    target_x, target_y = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
                    if constants.DEMO_MODE:
                        # Start visual Dijkstra demonstration
                        if (0 <= target_x < MAP_WIDTH and 0 <= target_y < MAP_HEIGHT 
                            and terrain_map[target_y][target_x] > 0):
                            start = (player_hero.x, player_hero.y)
                            goal = (target_x, target_y)
                            dijkstra_generator = dijkstra_visual(start, goal, terrain_map)
                            dijkstra_state = None
                            dijkstra_last_step_time = pygame.time.get_ticks()
                    else:
                        player_hero.set_target(target_x, target_y)

        # Process Dijkstra visualization steps in demo mode
        if dijkstra_generator is not None:
            current_time = pygame.time.get_ticks()
            if current_time - dijkstra_last_step_time >= DEMO_DELAY_MS:
                try:
                    dijkstra_state = next(dijkstra_generator)
                    dijkstra_last_step_time = current_time
                    
                    # When done, set the path and clean up
                    if dijkstra_state.get('done'):
                        if dijkstra_state.get('path'):
                            player_hero.path = dijkstra_state['path'][1:]  # Exclude start
                        dijkstra_generator = None
                except StopIteration:
                    dijkstra_generator = None

        player_hero.update(moves)

        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        
        draw_map_objects(event_map)
        
        # Draw Dijkstra visualization overlay
        draw_dijkstra_visualization(dijkstra_state)
        
        player_hero.draw(screen)
        enemy_hero.draw(screen)


        Resources.draw_resources(screen, resources)
        draw_date(screen)
        draw_army(screen, player_hero)
        moves.draw(screen, MAP_WIDTH * TILE_SIZE + 60, MAP_HEIGHT * TILE_SIZE - 100)
        draw_demo_mode_indicator()
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
            211: lambda: fight(player_hero),
            212: lambda: fight(player_hero),
            213: lambda: fight(player_hero),
            214: lambda: fight(player_hero),
            221: lambda: fight(player_hero),
            222: lambda: fight(player_hero),
            223: lambda: fight(player_hero),
            224: lambda: fight(player_hero),
            230: lambda: fight(player_hero),
        }

        if event_map[player_hero.y][player_hero.x]>20:
            if event_map[player_hero.y][player_hero.x] in event_dictionary:
                event_dictionary[event_map[player_hero.y][player_hero.x]]()
                if event_map[player_hero.y][player_hero.x] >=20 and event_map[player_hero.y][player_hero.x] <=100 or event_map[player_hero.y][player_hero.x]>=200: 
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