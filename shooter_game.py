from pygame import *
from random import *
from time import time as timer

win_width = 1000
win_height = 1000
window = display.set_mode((win_height, win_width))
display.set_caption('kazah simulatior')

background = transform.scale(image.load('galaxy.jpg'), (win_height, win_width))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg') 

font.init()
number_font = font.Font(None, 36)
over_font = font.Font(None, 80)
game_over_text = over_font.render('Пришло время оплаты штрафа!', 1, (40, 80, 100))
win_text = over_font.render('Вы укрылись от штрафа!', 1, (28, 90, 200))

number = 0
maximal_number =12


#классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Kazah_man(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            
    
    def fire(self):
        kumisa = Kumis('bullet.png', self.rect.centerx, self.rect.top, 7, 10, 10)
        kumis.add(kumisa)

class Kumis(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global number
        if self.rect.y > win_height:
            number += 1
            self.rect.y = 0
            self.rect.x = randint(90, win_width - 80)


class Povistka(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(90, win_width - 80)

num_kure = 0
rel_time = False



    

player_kazah = Kazah_man('rocket.png', 5, win_height - 300, 80, 90, 10)

kumis = sprite.Group()
shtrafs = sprite.Group()
for i in range(5):
    shtraf = Enemy('ufo.png', randint(10, win_width - 100), -80, 80, 40, randint(1, 2))
    shtrafs.add(shtraf)

povistkas = sprite.Group()
for i in range(5):
    povistka = Povistka('asteroid.png', randint(10, win_width - 100), -80, 80, 40, randint(1, 1))
    povistkas.add(povistka)





game = True
finish = False
scare = 0
win_scare = 10

while game:
    window.blit(background, (0, 0))

    text_lose = number_font.render('надо оплатить:' + str(number), 100, (250, 250, 250))
    window.blit(text_lose, (10, 20))
    
    text_bah = number_font.render('отклонили:' + str(scare), 100, (250, 250, 250)) 
    window.blit(text_bah, (10, 40))

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:

                if num_kure < 5 and rel_time == False:
                    num_kure += 1
                    player_kazah.fire()

                if num_kure >= 5 and rel_time == False:
                    start_time = timer()
                    rel_time = True 


    if not finish:
        player_kazah.reset()
        

        shtrafs.draw(window)
        kumis.draw(window)
        povistkas.draw(window)


        if rel_time == True:
            end_time = timer()

            if end_time - start_time < 3:
                reload_text  = number_font.render('переливание кумыса', 1, (150, 180, 200))
                window.blit(reload_text, (200, 500))
            else:
                num_kure = 0
                rel_time = False

        collides = sprite.groupcollide(shtrafs, kumis, True, True)
        for collide in collides:
            scare += 1
            shtraf = Enemy('ufo.png', randint(10, win_width - 100), -80, 80, 40, randint(1, 3))
            shtrafs.add(shtraf)

        if scare >= win_scare:
            finish = True 
            window.blit(win_text, (200, 300))

        if sprite.spritecollide(player_kazah, shtrafs, False) or sprite.spritecollide(player_kazah, povistkas, False) or number >= maximal_number:
            finish = True 
            window.blit(game_over_text, (185, 300))         

        povistkas.update()
        shtrafs.update()
        kumis.update()
        player_kazah.update()
        display.update()
    
    else:

        time.delay(3000)
        
        
        for shtraf in shtrafs:
            shtraf.kill()
        
        for povistka in povistkas:
            povistka.kill()

        for kumis_bullet in kumis:  
            kumis_bullet.kill()
        
        scare = 0
        number = 0
 
        for i in range(5):
            shtraf = Enemy('ufo.png', randint(10, win_width - 100), -80, 80, 40, randint(1, 5))
            shtrafs.add(shtraf)
        
        finish = False 