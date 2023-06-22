import pygame
import os
from constants import *

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
        if target_y>=MAP_HEIGHT or target_y<0:
            return
        if target_x>=MAP_WIDTH or target_x<0:
            return
        if map[target_y][target_x] <= 0:
            return
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

class House: 
    def __init__(self, x, y, image_path):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', image_path)), (TILE_SIZE*3, TILE_SIZE*2))
        self.x = x
        self.y = y
    def draw(self, screen):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))


class Resources:
    def __init__(self):
        self.meowcoins = 0
        self.milk = 0
        self.fish = 0

    def draw_resources(screen, resources):

        font = pygame.font.Font(None, 24)

        meowcoins_text = font.render('MeowCoins: ' + str(resources.meowcoins), True, (0, 0, 0))
        screen.blit(meowcoins_text, (MAP_WIDTH * TILE_SIZE + 20, 50))

        milk_text = font.render('Milk: ' + str(resources.milk), True, (0, 0, 0))
        screen.blit(milk_text, (MAP_WIDTH * TILE_SIZE + 20, 80))

        fish_text = font.render('Fish: ' + str(resources.fish), True, (0, 0, 0))
        screen.blit(fish_text, (MAP_WIDTH * TILE_SIZE + 20, 110))

