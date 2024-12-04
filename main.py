from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
pew_pew = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None, 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        pass

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

win_width = 700
win_height = 500
display.set_caption("Half Shot Shooters")
window = display.set_mode((700, 500))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 4)
goobers = sprite.Group()
for i in range(1, 6):
    goober = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    goobers.add(goober)

finish = False
game = True



while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
       
    if not finish:
        window.blit(background,(0, 0))
        
        text = font2.render("score:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font2.render("missed:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        ship.update()
        goobers.update()

        ship.reset()
        goobers.draw(window)

        display.update()

    time.delay(50)
