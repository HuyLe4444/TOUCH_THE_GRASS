import pygame
import sys
pygame.font.init()

WIDTH, HEIGHT = 300, 200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TOUCH_THE_GRASS!!!")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
S_RED = (196, 46, 28)

GRASS = pygame.image.load('grass.png')
TOUCH_BUTTON = pygame.image.load('Button.png').convert_alpha()

FONT_CLICKED = pygame.font.SysFont('comicsans', 18)

BUTTON_CLICKED = pygame.USEREVENT + 1

class Button():
    def __init__(self, pos_x, pos_y, image, scale):
        i_width = image.get_width()
        i_height = image.get_height()
        self.image = pygame.transform.scale(image, (int(i_width * scale), int(i_height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.clicked = False
        
    def draw(self):
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                pygame.event.post(pygame.event.Event(BUTTON_CLICKED))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        

touch_button = Button(130, 50, TOUCH_BUTTON, 2)


class Grass(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.is_animating = False
        self.sprites = []
        self.sprites.append(pygame.image.load('frame_0.png'))
        self.sprites.append(pygame.image.load('frame_1.png'))
        self.sprites.append(pygame.image.load('frame_2.png'))
        self.sprites.append(pygame.image.load('frame_3.png'))
        self.sprites.append(pygame.image.load('frame_4.png'))
        self.curr_sprite = 0
        self.image = self.sprites[self.curr_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        
    def update(self):
        if self.is_animating == True:
            self.curr_sprite += 0.7
            
            if self.curr_sprite >= len(self.sprites):
                self.curr_sprite = 0
                self.is_animating = False
                
            self.image = self.sprites[int(self.curr_sprite)]
        
    def animate(self): 
        self.is_animating = True
        
        
moving_sprites = pygame.sprite.Group()
grass = Grass(10, 10)
moving_sprites.add(grass)

def draw_window(times_clicked):
    WIN.blit(GRASS, (0, 0))
    
    text = FONT_CLICKED.render("You touch the grass: " + str(times_clicked) + " time(s)", 1, BLACK)
    WIN.blit(text, (20, 150))
    
    moving_sprites.draw(WIN)
    moving_sprites.update()
    touch_button.draw()
    pygame.display.update()


def main():
    times_clicked = 0
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == BUTTON_CLICKED:
                grass.animate()
                times_clicked += 1
    
        draw_window(times_clicked)            
    
if __name__ == "__main__":
    main()