import pygame


class MovesCounter:
    def __init__(self, starting_moves=10):
        self.moves = starting_moves
        self.max_moves = starting_moves

    def draw(self, screen, x, y):
        font = pygame.font.Font(None, 24)
        # Display moves with 1 decimal place
        text = font.render(f'Energy: {int(self.moves)}', True, (0, 0, 0))
        screen.blit(text, (x, y))


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.color = color
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, outline=None):
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