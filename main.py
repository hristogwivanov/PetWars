import pygame
import os

# Constants
TILE_SIZE = 100
MAP_WIDTH = 14
MAP_HEIGHT = 10

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
BLACK = (0, 0, 0)




class Hero:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', image_path)), (TILE_SIZE, TILE_SIZE))

    def draw(self, screen):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def set_target(self, target_x, target_y):
        if abs(self.x - target_x) + abs(self.y - target_y) == 1:
            self.target_x = target_x
            self.target_y = target_y

    def update(self, moves_counter):
        if moves_counter.moves <= 0:
            return

        if self.x < self.target_x:
            self.x += 1
            moves_counter.moves -= 1
        elif self.x > self.target_x:
            self.x -= 1
            moves_counter.moves -= 1

        if self.y < self.target_y:
            self.y += 1
            moves_counter.moves -= 1
        elif self.y > self.target_y:
            self.y -= 1
            moves_counter.moves -= 1
    
    def reset_target(self):
        self.target_x = self.x
        self.target_y = self.y


class Resources:
    def __init__(self):
        self.milk = 0
        self.fish = 0
        self.meowcoin = 0

    def draw_resources(screen, resources):

        font = pygame.font.Font(None, 24)

        meowcoin_text = font.render('MeowCoin: ' + str(resources.meowcoin), True, (0, 0, 0))
        screen.blit(meowcoin_text, (MAP_WIDTH * TILE_SIZE + 20, 50))

        milk_text = font.render('Milk: ' + str(resources.milk), True, (0, 0, 0))
        screen.blit(milk_text, (MAP_WIDTH * TILE_SIZE + 20, 90))

        fish_text = font.render('Fish: ' + str(resources.fish), True, (0, 0, 0))
        screen.blit(fish_text, (MAP_WIDTH * TILE_SIZE + 20, 130))




class MovesCounter:
    def __init__(self, starting_moves=3):
        self.moves = starting_moves

    def draw(self, screen, x, y):
        font = pygame.font.Font(None, 24)
        text = font.render(f'Moves: {self.moves}', True, (0, 0, 0))
        screen.blit(text, (x, y))


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.color = color
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4), 0)

        pygame.draw.rect(screen, self.color, self.rect)
        
        if self.text != '':
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.rect.x + (self.rect.width // 2 - text.get_width() // 2), self.rect.y + (self.rect.height // 2 - text.get_height() // 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if self.rect.collidepoint(pos):
            return True
        return False


def main():


    
    pygame.init()


    screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE + 200, MAP_HEIGHT * TILE_SIZE))
    clock = pygame.time.Clock()

    background = pygame.image.load(os.path.join('images', 'map.png'))
    background = pygame.transform.scale(background, (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))



    map = [
        [0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 123, 0, 21, 0, 0, 0, 0, 0, 126, 251, 0, 12, 0],
        [1, 1, 1, 203, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 210, 1, 0, 0, 0],
        [21, 202, 1, 1, 0, 0, 0, 212, 0, 0, 1, 0, 21, 26],
        [22, 23, 0, 1, 0, 0, 0, 30, 0, 0, 1, 1, 252, 21],
        [0, 0, 0, 1, 0, 0, 0, 28, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 211, 1, 1, 253, 1, 1, 0],
        [0, 11, 0, 1, 0, 0, 0, 0, 0, 0, 21, 0, 127, 0],
        [1, 1, 1, 1, 201, 122, 0, 0, 0, 0, 26, 0, 0, 0],

    ]

    player_hero = Hero(0, MAP_HEIGHT-1, 'hero.png')  # Assumes a 'hero.png' in your images directory
    enemy_hero = Hero(MAP_WIDTH-1, 0, 'enemy.png')  # Assumes an 'enemy.png' in your images directory

    win_dialog_frame = pygame.Rect(MAP_WIDTH * TILE_SIZE / 2 - 130, (MAP_HEIGHT * TILE_SIZE) / 2 - 90, 260, 180)


    font = pygame.font.Font(None, 50)
    win_text = font.render('You win!', True, (0, 0, 0))
    win_text_position = win_text.get_rect(center=(win_dialog_frame.width//2, win_dialog_frame.height//2 - 40))  # reduce Y value to move text up
    screen.blit(win_text, (win_dialog_frame.x + win_text_position.x, win_dialog_frame.y + win_text_position.y))
    ok_button = Button(MAP_WIDTH * TILE_SIZE / 2 - 40, (MAP_HEIGHT * TILE_SIZE) / 2 + 10, 80, 40, LIGHT_BLUE, 'OK')
    show_win_dialog = False

    moves = MovesCounter(3)
    end_turn_button = Button(MAP_WIDTH * TILE_SIZE + 60, MAP_HEIGHT * TILE_SIZE - 50, 80, 40, LIGHT_BLUE, 'End Turn')



    def draw_grid(screen):
        for x in range(0, MAP_WIDTH * TILE_SIZE, TILE_SIZE):
            for y in range(0, MAP_HEIGHT * TILE_SIZE, TILE_SIZE):
                pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 1)

    def draw_tile_numbers(screen):
        font = pygame.font.Font(None, 24)
        number = 1
        for y in range(MAP_HEIGHT-1, -1, -1):  # start from the bottom
            for x in range(MAP_WIDTH):
                text = font.render(str(number), True, (0, 0, 0))
                screen.blit(text, (x * TILE_SIZE + TILE_SIZE / 2 - text.get_width() / 2, y * TILE_SIZE + TILE_SIZE / 2 - text.get_height() / 2))
                number += 1


    def draw_resources(screen, resources):
        font = pygame.font.Font(None, 24)

        milk_text = font.render('Milk: ' + str(resources.milk), True, (0, 0, 0))
        screen.blit(milk_text, (MAP_WIDTH * TILE_SIZE + 20, 50))

        fish_text = font.render('Fish: ' + str(resources.fish), True, (0, 0, 0))
        screen.blit(fish_text, (MAP_WIDTH * TILE_SIZE + 20, 80))

        meowcoin_text = font.render('MeowCoin: ' + str(resources.meowcoin), True, (0, 0, 0))
        screen.blit(meowcoin_text, (MAP_WIDTH * TILE_SIZE + 20, 110))



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

        screen.fill(WHITE)
        draw_grid(screen)
        screen.blit(background, (0, 0))
        draw_tile_numbers(screen)
        player_hero.draw(screen)
        enemy_hero.draw(screen)
        draw_resources(screen, resources)
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