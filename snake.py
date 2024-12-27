from pygame.locals import *
import pygame
import time
from random import randint

class Player:
    x = 0
    y = 0 
    d = 0
    positions = []
    length = 4

class Apple:
    x = 0
    y = 0

class Game:
    game_width = 10
    game_height = 10
    grid_size = 44

    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False

    def __init__(self):
        self._running = True
        self.player = Player()
        self.apple = Apple()

        self.apple.x = randint(0,self.game_width) * self.grid_size
        self.apple.y = randint(0,self.game_height) * self.grid_size

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((640,480), pygame.HWSURFACE)
        pygame.display.set_caption('Pygame example')
        self._snake_image = pygame.image.load("snake.png").convert()
        self._apple_image = pygame.image.load("apple.png").convert()
        self.name_font = pygame.font.SysFont('Helvetica', 40)
        self.game_over_font = pygame.font.SysFont('Verdana', 50)

    def on_render(self):
        self._display_surf.fill((0,0,0))

        for pos in self.player.positions:
            self._display_surf.blit(self._snake_image, (pos[0],pos[1])) 

        self._display_surf.blit(self._apple_image, (self.apple.x,self.apple.y))

        name = self.name_font.render("Snake Game by Avidz", True, (255,55,55))
        self._display_surf.blit(name, (0,400))

        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()

    def snake_logic(self):
        if self.player.d == 0:
            self.player.x += 44
        elif self.player.d == 1:
            self.player.x -= 44
        elif self.player.d == 2:
            self.player.y -= 44
        elif self.player.d == 3:
            self.player.y += 44

        if len(self.player.positions) < self.player.length:
            self.player.positions.append((self.player.x,self.player.y))
        else:
            self.player.positions.pop(0)
            self.player.positions.append((self.player.x,self.player.y))

    def game_play_logic(self):
        if self.isCollision(self.player.x,self.player.y,self.apple.x,self.apple.y, 44):
            print('devours')
            self.apple.x = randint(0,self.game_width) * self.grid_size
            self.apple.y = randint(0,self.game_height) * self.grid_size
            self.player.length += 1

        if len(self.player.positions) > self.player.length-1:
            for i in range(0,self.player.length-1):                    
                if self.isCollision(self.player.x,self.player.y,self.player.positions[i][0], self.player.positions[i][1],40):
                    print('GAME OVER')
                    self.display_game_over()
                    exit()

    def game_logic(self):
        self.snake_logic()
        self.game_play_logic()                

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                
        keys = pygame.key.get_pressed() 
        
        if keys[K_RIGHT]:
            self.player.d = 0

        if keys[K_LEFT]:
            self.player.d = 1

        if keys[K_UP]:
            self.player.d = 2

        if keys[K_DOWN]:
            self.player.d = 3

    def display_game_over(self):
        # Create the Game Over screen
        self._display_surf.fill((0, 0, 0))
        game_over_text = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.game_over_font.render(f"Score: {self.player.length}", True, (0, 255, 0))
        thanks_text = self.name_font.render("Thanks for playing!", True, (255, 255, 255))
        avidz_text = self.name_font.render("Simple game by Avidz", True, (255, 255, 255))

        self._display_surf.blit(game_over_text, (180, 100))
        self._display_surf.blit(score_text, (200, 180))
        self._display_surf.blit(thanks_text, (150, 260))
        self._display_surf.blit(avidz_text, (150, 320))

        pygame.display.flip()
        time.sleep(3)  # Show the screen for 3 seconds before quitting
        self.on_cleanup()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while self._running:
            self.handle_events()
            self.game_logic()
            self.on_render()
            time.sleep(0.1)
  
        self.on_cleanup()
 
if __name__ == "__main__" :
    game = Game()
    game.on_execute()
