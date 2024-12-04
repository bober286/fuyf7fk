from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
pew_pew = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('you win', True, (255, 255, 255))
lose = font1.render('you lose', True, (180, 0, 0))
font2 = font.Font(None, 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'

score = 0
goal = 10
lost = 0
max_lost = 3

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
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


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

bullets = sprite.Group()
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                pew_pew.play()
                ship.fire()
        if not finish:
            window.blit(background,(0, 0))
            
            ship.update()
            goobers.update()
            bullets.update()

            ship.reset()
            goobers.draw(window)
            bullets.draw(window)
            collides - sprite.groupcollide(goobers, bullets, True, True)
            for c in collides:
                score = score + 1
                goober = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                goobers.add(goober)
            if sprite.spritecollide(ship, goobers, False) or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))
                if score >= goal:
                    finish = True
                    window.blit(win, (200, 200))
                    
                    text = font2.render("score:" + str(score), 1, (255, 255, 255))
                    window.blit(text, (10, 20))
                    
                    text_lose = font2.render("missed:" + str(score), 1, (255, 255, 255))
                    window.blit(text, (10, 20))

            display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for g in goobers:
            g.kill()
            
            time.delay(3000)
            for i in range(1, 6):
                goober = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                goobers.add(goober)
    time.delay(50)
