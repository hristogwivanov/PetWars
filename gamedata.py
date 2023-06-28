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
        if terrain_map[target_y][target_x] <= 0:
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
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', image_path)), (TILE_SIZE*2.5, TILE_SIZE*2.5))
        self.x = x+0.1
        self.y = y-0.5
    def draw(self, screen):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))


class Resources:
    def __init__(self):
        self.meowcoins = 0
        self.milk = 0
        self.fish = 0
        self.meowcoinproduction = 1000
        self.milkproduction = 0
        self.fishproduction = 0

    def draw_resources(screen, resources):

        font = pygame.font.Font(None, 24)

        resources_text = font.render('Resources', True, (0, 0, 0))
        screen.blit(resources_text, (MAP_WIDTH * TILE_SIZE + 60, 10))

        meowcoins_text = font.render('MeowCoins: ' + str(resources.meowcoins), True, (0, 0, 0))
        screen.blit(meowcoins_text, (MAP_WIDTH * TILE_SIZE + 20, 50))

        milk_text = font.render('Milk: ' + str(resources.milk), True, (0, 0, 0))
        screen.blit(milk_text, (MAP_WIDTH * TILE_SIZE + 20, 80))

        fish_text = font.render('Fish: ' + str(resources.fish), True, (0, 0, 0))
        screen.blit(fish_text, (MAP_WIDTH * TILE_SIZE + 20, 110))

    def update_resources(resources):
        resources.meowcoins += resources.meowcoinproduction
        resources.milk += resources.milkproduction
        resources.fish += resources.fishproduction



##### LEGACY CODE - This was changed in order to make the events depend on the event map instead of instances of the objects created in the main loop.

# class Resource: 
#     def __init__(self, x, y, type, quantity):
#         match type:            
#             case 'meowcoins':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'meowcoins.png')), (TILE_SIZE, TILE_SIZE))
#             case 'fish':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'fish.png')), (TILE_SIZE, TILE_SIZE))
#             case 'dogecoins':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'dogecoins.png')), (TILE_SIZE, TILE_SIZE))
#             case 'bones':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'bones.png')), (TILE_SIZE, TILE_SIZE))
#             case 'meat':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'meat.png')), (TILE_SIZE, TILE_SIZE))
#             case _:
#                 pass
#         self.x = x
#         self.y = y
#         self.type = type
#         self.quantity = quantity

#     def draw(self, screen):
#         screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

# class Milk(Resource):
#     def __init__(self, x, y, quantity):
#         super().__init__(x, y, 'milk', quantity)
#            self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'milk.png')), (TILE_SIZE, TILE_SIZE))
        



# class Farm:
#     def __init__(self, x, y, type):
#         match type:            
#             case 'milk':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'milkfarm.png')), (TILE_SIZE*2, TILE_SIZE*2))
#             case 'fish':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'fishpound.png')), (TILE_SIZE, TILE_SIZE))
#             case 'bones':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'boneyard.png')), (TILE_SIZE, TILE_SIZE))
#             case 'meat':
#                 self.image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'pigfarm.png')), (TILE_SIZE, TILE_SIZE))
#             case _:
#                 pass  
#         self.x = x
#         self.y = y
#         self.type = type

#     def draw(self, screen):
#         screen.blit(self.image, (self.x * TILE_SIZE, (self.y-1) * TILE_SIZE))
        
##### DrawHouses #####

def drawCatHouse(x, y, screen):
    x = x - 0.9
    y = y - 1.5
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'CatHouse.png')), (TILE_SIZE*2.5, TILE_SIZE*2.5))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawDogHouse(x, y, screen):
    x = x - 0.6
    y = y - 1.5
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'DogHouse.png')), (TILE_SIZE*2.5, TILE_SIZE*2.5))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

##### Resources drawing and events #####

def drawGold(x, y, screen): 
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'meowcoins.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def getGold(qty, resources): 
    resources.meowcoins+=qty

def drawMilk(x, y, screen): 
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'milk.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def getMilk(qty, resources): 
    resources.milk+=qty
    
def drawFish(x, y, screen): 
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'fish.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def getFish(qty, resources): 
    resources.fish+=qty

def drawDoge(x, y, screen): 
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'dogecoins.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def getDoge(qty, resources): 
    pass

def drawBones(x, y, screen): 
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'bones.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def getBones(qty, resources): 
    pass

def drawMeat(x, y, screen): 
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'meat.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def getMeat(qty, resources): 
    pass

##### Farms drawing and events #####

def visitMilkFarm(resources):
    resources.milkproduction = 2

def drawMilkFarm(x, y, screen):
    y = y - 1
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'milkfarm.png')), (TILE_SIZE*2, TILE_SIZE*2))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def visitFishPound(resources):
    resources.fishproduction = 1

def drawFishPound(x, y, screen):
    y = y - 1
    x = x - 1
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'fishpound.png')), (TILE_SIZE*2, TILE_SIZE*2))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def visitBoneYard(resources):
    resources.bonesproduction = 2

def drawBoneYard(x, y, screen):
    y = y - 1
    x = x - 1
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'boneyard.png')), (TILE_SIZE*2, TILE_SIZE*2))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def visitPigFarm(resources):
    resources.meatproduction = 1

def drawPigFarm(x, y, screen):
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'pigfarm.png')), (TILE_SIZE*2, TILE_SIZE*2))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))


##### Neutral armies drawing and events #####

def drawMouse(x, y, screen):
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'mouse.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawFlippedMouse(x, y, screen):
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'mouse.png')), (TILE_SIZE, TILE_SIZE))
    image = pygame.transform.flip(image, True, False)
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawStreetCat(x, y, screen):
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'streetcat.png')), (TILE_SIZE, TILE_SIZE))
    image = pygame.transform.flip(image, True, False)
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawPersianCat(x, y, screen):
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'persiancat.png')), (TILE_SIZE, TILE_SIZE))
    image = pygame.transform.flip(image, True, False)
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawSphynxCat(x, y, screen):
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'sphynxcat.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawPugDog(x, y, screen):
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'pugdog.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawMalinoisDog(x, y, screen):      
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'malinoisdog.png')), (TILE_SIZE, TILE_SIZE))
    image = pygame.transform.flip(image, True, False)
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawShibaInuDog(x, y, screen):      
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'shibainudog.png')), (TILE_SIZE, TILE_SIZE))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def drawDragon(x, y, screen):      
    y=y-0.5
    x=x-0.2
    image = pygame.transform.scale(pygame.image.load(os.path.join('images', 'dragon.png')), (TILE_SIZE*1.5, TILE_SIZE*1.5))
    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def date_update():
    date['day'] += 1
    if date['day'] > 7:
        date['day'] = 1
        date['week'] += 1
        if date['week'] > 4: 
            date['week'] = 1
            date['month'] += 1
            if date['month'] >12: date['month'] = 0

def draw_date(screen):
    font = pygame.font.Font(None, 24)
    calendar_text = font.render('Calendar', True, (0, 0, 0))
    screen.blit(calendar_text, (MAP_WIDTH * TILE_SIZE + 60, 760))
    day_text = font.render('Day: ' + str(day_dictionary[date['day']]), True, (0, 0, 0))
    screen.blit(day_text, (MAP_WIDTH * TILE_SIZE + 20, 800))
    week_text = font.render('Week: ' + str(week_dictionary[date['week']]), True, (0, 0, 0))
    screen.blit(week_text, (MAP_WIDTH * TILE_SIZE + 20, 830))
    month_text = font.render('Month: ' + str(month_dictionary[date['month']]), True, (0, 0, 0))
    screen.blit(month_text, (MAP_WIDTH * TILE_SIZE + 20, 860))

def end_of_turn(resources, moves, player_hero):
    date_update()
    resources.update_resources()
    moves.moves = 3
    player_hero.reset_target()
