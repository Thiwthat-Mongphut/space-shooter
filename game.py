# Art from kenney in opengameart.org
# Sound from Jan125 in opengameart.org
#---------------------------------------
#       from Volvion in freesound.org
#---------------------------------------

import pygame
import random
#---------------------------------------
import time
#---------------------------------------
from os import path

#---------------------------------------
boss_difficult = 1
boss_count = 0
#---------------------------------------

# Screen Setting
width = 480
height = 720
fps = 60
powerup_time = 5000

# Color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

#---------------------------------------
pink_red = (183, 28, 28)
#---------------------------------------

#star bg
stars_bg_list1 = [[random.randint(0, width), random.randint(0, height)] for x in range(150)]
stars_bg_list2 = [[random.randint(0, width), random.randint(0, height)] for x in range(50)]


# Set up folder
def get_hs(new=None):
    hs_folder = path.join(path.dirname(__file__))
    if new is None:
        with open(path.join(hs_folder, 'highscore.txt'), 'r') as f:
            try:
                highscore = int(f.read())
            except:
                highscore = 0 
        return highscore
    else:
        with open(path.join(hs_folder, 'highscore.txt'), 'w' ) as f:
            f.write(str(new))
            f.close()

img_folder = path.join(path.dirname(__file__), 'pic')
snd_folder = path.join(path.dirname(__file__), 'sound') 
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('bangna-new')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_hp_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0

    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    ountline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, ountline_rect, 2)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (73, 73))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.hp = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):

        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # unhide if hiden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10


        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -9
        if keystate[pygame.K_RIGHT]:
            self.speedx = 9
        self.rect.x += self.speedx

        if keystate[pygame.K_DOWN]:
            self.speedy = 9
        if keystate[pygame.K_UP]:
            self.speedy = -9
        self.rect.y += self.speedy

        if keystate[pygame.K_SPACE]:
            self.shoot()

        if not self.hidden:
            if self.rect.right > width:
                self.rect.right = width
            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.bottom > height:
                self.rect.bottom = height
            if self.rect.top < 0:
                self.rect.top = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now

            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10000

class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.init_pos = [150, 200, 200, 250,
        #                  245, 250, 300, 300, 350]
        self.image_orig = random.choice(meteor_img)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(70, 410, 45)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = 0
        self.speedy = 5
        self.rot = 0
        #self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1100,1600)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = mobBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            mobbullets.add(bullet)

    def update(self):
        # self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.shoot()

        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(70, 410, 45)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 5
                   
class Power(pygame.sprite.Sprite):

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['hp', 'gun'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy

        if self.rect.top > height:
            self.kill()

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        #-----------------------------------------
        self.radius = self.rect.width / 2 * 0.8
        #-----------------------------------------
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()

class mobBullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletred_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        #-----------------------------------------
        self.radius = self.rect.width / 2 * 0.8
        #-----------------------------------------
        self.speedy = random.randrange(7, 9)

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom > height:
            self.kill()

class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        #------------------------------------------------
        self.radius = self.rect.w / 2 * 0.6
        #------------------------------------------------
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def button(x,y,w,h):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, black, (x,y,w,h),1)
    if x + w > mouse_pos[0] and x < mouse_pos[0] and y+h > mouse_pos[1] and y < mouse_pos[1]:
        if mouse_click[0] == 1:
            return True

def main_menu(x):
    pygame.display.flip()
    highscore = get_hs()
    if x == 3:

        draw_text(screen, 'START', 30, width / 2, 480)
        draw_text(screen, 'HIGH SCORE: ' + str(highscore), 30, width / 2, 510)
        draw_text(screen, 'EXIT', 30, width / 2, 540)
        for star in stars_bg_list1:
            pygame.draw.rect(screen, white, (star[0], star[1], 1,1), 0)
            star[1] = star[1] + 1
            if star[1] > height :
                star[1] = -10
                star[0] = random.randint(0, width)
        for star in stars_bg_list2:
            pygame.draw.circle(screen, white, (star[0], star[1]), 2, 0)
            star[1] = star[1] + 2
            if star[1] > height :
                star[1] = -10
                star[0] = random.randint(0, width)

        waiting = True
        while waiting:
            clock.tick(fps)
            for event in pygame.event.get():
                if button(200,475,80,25):
                    waiting = False
                if button(212,538,55,23):
                    pygame.quit()
                    quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            screen.blit(logo, (25, 100))
            pygame.display.update()

def game_over_scr():
    highscore = get_hs()
    draw_text(screen, 'GAME OVER', 60, width / 2, height *0.25)
    draw_text(screen, 'TRY AGAIN', 30, width/2, 550)
    print(highscore)
    print(score)
    if score > highscore:
        highscore = score
        draw_text(screen, 'NEW HIGH SCORE', 40, width / 2, height / 2 + 50)
        get_hs(highscore)
    else:
        draw_text(screen, 'HIGH SCORE: ' + str(highscore), 40, width / 2, height / 2 + 50)

    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if button(180,550,120,20):
                screen.fill(black)
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                #screen.blit(logo, (0, 0))
        pygame.display.update()

    
    
    

    
        

# Graphic
#bg = pygame.image.load(path.join(img_folder, 'menu.jpg')).convert()
#bg_rect = bg.get_rect()
logo = pygame.image.load(path.join(img_folder, 'logo.png')).convert_alpha()
#logo_rect = logo.get_rect()

player_img = pygame.image.load(path.join(img_folder, 'plane.png')).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
bullet_img = pygame.image.load(path.join(img_folder, 'laserBlue.png')).convert_alpha()
bulletred_img = pygame.image.load(path.join(img_folder, 'laserRed.png')).convert_alpha()

meteor_img = []
meteor_list = ['m1.png', 'm2.png', 'm3.png',
               'm4.png', 'm5.png', 'm6.png', 'm7.png', 'm8.png']
for img in meteor_list:
    meteor_img.append(pygame.image.load(path.join(img_folder, img)).convert_alpha())

explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
#--------------Boss------------------
explosion_animation['sulg'] = []
#--------------Boss------------------
explosion_animation['player'] = []
for i in range(9):
    filename = 'e{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animation['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animation['sm'].append(img_sm)

    #---------------------------Boss-------------------------
    img_lg = pygame.transform.scale(img, (180, 180))
    explosion_animation['sulg'].append(img_lg)
    #---------------------------Boss--------------------------

    filename = 'sx{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
    img.set_colorkey(black)
    explosion_animation['player'].append(img)

powerup_img = {}
powerup_img['hp'] = pygame.image.load(
    path.join(img_folder, 'hp.png')).convert_alpha()
powerup_img['gun'] = pygame.image.load(
    path.join(img_folder, 'gun.png')).convert_alpha()

#--------------------------- Start Boss edit --------------------------

img_boss = []
img_boss_damaged = []
img_boss_bullet = {}
for i in range(3):
    img_boss_bullet[str(i)] = []

for i in range(3):
    if i == 2:
        for i in range(3):
            filename = 'b2_{}.png'.format(i)
            image = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
            image.set_colorkey(black)
            img_boss.append(image)

        for i in range(5):
            filename = 'bb2_{}.png'.format(i)
            image = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
            image.set_colorkey(black)
            img_boss_bullet['2'].append(image)

        image = pygame.image.load(path.join(img_folder, 'bd2.png')).convert_alpha()
        image.set_colorkey(black)
        img_boss_damaged.append(image)

    else:
        filename = 'b{}.png'.format(i)
        image = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
        img_boss.append(image)

        filename = 'bd{}.png'.format(i)
        image = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
        img_boss_damaged.append(image)

        filename = 'bb{}.png'.format(i)
        image = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
        img_boss_bullet[str(i)].append(image)
        if i == 1:
            image = pygame.image.load(path.join(img_folder, 'bb10.png')).convert_alpha()
            img_boss_bullet['1'].append(image)


def BossCalling(order):
    if order == 0:
        return Boss_0()
    elif order == 1:
        return Boss_1()
    elif order == 2:
        return Boss_2()

class Boss_0(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss[0]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.top = width / 2, -80
        self.radius = self.rect.width / 2 * 0.8
        self.direction = 1
        self.pattern = 1
        self.hp = 200
        self.ori_hp = self.hp
        self.ulti = 1
        self.ori_ulti = self.ulti
        self.hit_color_delay = pygame.time.get_ticks()
        self.skill_cooldown = pygame.time.get_ticks()

    def bullet(self):
        if self.pattern == 1:
            B0P1(1)
        elif self.pattern == 2:
            B0P2()
        elif self.pattern == 3:
            B0P3()
            B0P3()
        elif self.pattern == 4:
            self.pattern = 1
            B0P1(1)

    def appear(self):
        self.rect.y += 1

    def update(self):
        if self.ulti <= 0 and self.pattern == 3:
            self.ulti = self.ori_ulti

class B0P1(pygame.sprite.Sprite):

    def __init__(self, n):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['0'][0]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.7 / 2)
        self.hp = 6
        self.speed = 5 + boss_difficult

        if n == 1:
            self.rect.centerx = width / 4
            self.rect.y = curBoss.rect.bottom
            B0P1(2)
        else:
            self.rect.centerx = width - (width / 4)
            self.rect.y = curBoss.rect.bottom

        boss_bullet.add(self)
        all_sprites.add(self)

    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= height + 10:
            self.kill()
        curBoss.skill_cooldown = pygame.time.get_ticks()

class B0P2(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['0'][0]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(
            (width - width / 3, width / 2, width / 3))
        self.rect.y = curBoss.rect.bottom
        self.radius = int(self.rect.width * 0.7 / 2)
        self.hp = 6
        self.speed = 4 + boss_difficult

        boss_bullet.add(self)
        all_sprites.add(self)

    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= height - (height / 4):
            self.kill()
            expl_sound.play()
            expl = Explosion(self.rect.center, 'sulg')
            all_sprites.add(expl)
            boss_bullet.add(expl)
        curBoss.skill_cooldown = pygame.time.get_ticks()

        if curBoss.hp <= curBoss.ori_hp / 3 and curBoss.ulti >= 1:
            if self.rect.y >= height - (height / 4):
                B0P2()
                curBoss.ulti -= 1
                curBoss.pattern += 1

class B0P3(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['0'][0]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice((width / 8, width / 8 * 7))
        self.rect.y = curBoss.rect.bottom
        self.radius = int(self.rect.width * 0.7 / 2)
        self.direction = 15 
        self.speed = 0 + boss_difficult
        self.hp = 4

        boss_bullet.add(self)
        all_sprites.add(self)

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.direction

        if self.rect.centerx <= width / 8:
            self.direction = 15
        elif self.rect.centerx >= width / 8 * 7:
            self.direction = -15
        if self.rect.y >= height + 10:
            self.kill()
        curBoss.skill_cooldown = pygame.time.get_ticks()

class Boss_1(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss[1]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.top = width / 2, -80
        self.radius = self.rect.width / 2 * 0.8
        self.direction = 1
        self.pattern = 1
        self.hp = 300 
        self.ori_hp = self.hp
        self.hit_color_delay = pygame.time.get_ticks()
        self.skill_cooldown = pygame.time.get_ticks()
        self.ulti = int(1)
        self.ori_ulti = self.ulti

    def bullet(self):
        if self.pattern == 1:
            divide = width / 8
            rectx = []
            for i in range(1, 8):
                rectx = i * divide
                B1P1(rectx)

        elif self.pattern == 2:
            B1P2()

        elif self.pattern == 3:
            x = width / 10
            y = curBoss.rect.bottom
            distance = 50

            for i in range(1, 11, 2):
                B1P3(x * i, y)
            for i in range(2, 9, 2):
                B1P3(x * i, y + 35)

        elif self.pattern == 4:
            self.pattern = 1

            divide = width / 8
            rectx = []
            for i in range(1, 8):
                rectx = i * divide
                B1P1(rectx)

    def appear(self):
        if self.pattern != 2:
            self.rect.y += 1

    def update(self):
        self.rect.x += self.direction
        if self.rect.centerx <= width / 2 - 20:
            self.direction = 1
        elif self.rect.centerx >= width / 2 + 20:
            self.direction = -1

        if self.ulti <= 0 and self.pattern == 3:
            self.ulti = self.ori_ulti

class B1P1(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['1'][0]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = curBoss.rect.bottom
        self.radius = int(self.rect.width * 0.85 / 2)
        self.hp = 2
        self.speed = 3 + boss_difficult

        boss_bullet.add(self)
        all_sprites.add(self)

    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= height + 10:
            self.kill()
        curBoss.skill_cooldown = pygame.time.get_ticks()

        if curBoss.hp <= curBoss.ori_hp / 3 and curBoss.ulti >= 1:
            if self.rect.y >= curBoss.rect.bottom + self.rect.height + 20:
                divide = width / 8
                rectx = []
                for i in range(1, 8):
                    rectx = i * divide
                    B1P1(rectx)
                curBoss.ulti -= 1

class B1P2(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['1'][1]
        self.image_orig = self.image
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = curBoss.rect.centerx + 5
        self.rect.y = curBoss.rect.bottom
        self.radius = int(self.rect.width * 0.85 / 2)
        self.hp = 15
        self.speed = 3 + boss_difficult
        self.rot = 0
        self.rot_speed = 30
        self.last_update = pygame.time.get_ticks()

        boss_bullet.add(self)
        all_sprites.add(self)

    def update(self):
        self.rect.y += self.speed
        self.rect.x += random.choice((self.speed, -self.speed))
        if self.rect.y >= height + 10:
            self.kill()
        curBoss.skill_cooldown = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_img = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class B1P3(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['1'][0]
        self.image_orig = self.image
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.radius = int(self.rect.width * 0.85 / 2)
        self.hp = 3
        self.speed = 4 + boss_difficult
        self.lock = 500
        self.timelock = 1500
        self.force = 1200
        self.startlock = pygame.time.get_ticks()

        boss_bullet.add(self)
        all_sprites.add(self)

    def update(self):
        curBoss.skill_cooldown = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.startlock > self.lock:
            if pygame.time.get_ticks() - self.startlock < self.force:
                if player.rect.y <= 0:
                    self.lockx = width / 2
                    self.locky = height
                else:
                    self.lockx = player.rect.centerx
                    self.locky = player.rect.y
            if self.rect.centerx < self.lockx:
                self.rect.centerx += self.speed
            else:
                self.rect.centerx -= self.speed
            if self.rect.y < self.locky:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed

            if pygame.time.get_ticks() - self.startlock > self.timelock:
                expl_sound.play()
                expl = Explosion(self.rect.center, 'lg')
                all_sprites.add(expl)
                boss_bullet.add(expl)
                self.kill()

class Bossbaria(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss[2]
        self.rect = self.image.get_rect()
        self.rect.centerx = curBoss.rect.centerx
        self.rect.y = curBoss.rect.bottom - 50
        self.radius = self.rect.height / 2 * 0.3
        self.direction = 1
        self.hp = 250
        self.status = True

        all_sprites.add(self)
        boss_baria.add(self)

    def update(self):
        self.rect.x += self.direction
        if self.rect.centerx <= width / 2 - 40:
            self.direction = 1
        elif self.rect.centerx >= width / 2 + 40:
            self.direction = -1

        if self.hp <= 0:
            self.status = False
            expl_sound.play()
            expl = Explosion(self.rect.center, 'sulg')
            all_sprites.add(expl)
            self.kill()

class Boss_2(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss[3]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.top = width / 2, -80
        self.radius = self.rect.width / 2 * 0.8
        self.pattern = 1
        self.radius = self.rect.width / 2 * 0.8
        self.direction = 1
        self.hp = 400
        self.hit_color_delay = pygame.time.get_ticks()
        self.skill_cooldown = pygame.time.get_ticks()
        # bullet controls
        self.wait_skill_two = pygame.time.get_ticks()
        self.next_bullet = pygame.time.get_ticks()
        self.shoot = 20 # number of bullets at pattern 1
        self.shoot_laser = False
        self.stop = False

    def appear(self):
        self.rect.y += 1

    def update(self):
        # boss moveing(left and right)
        self.rect.x += self.direction
        if self.rect.centerx <= width / 2 - 40:
            self.direction = 1
        elif self.rect.centerx >= width / 2 + 40:
            self.direction = -1

        # skill controls
        if self.pattern == 1:
            if pygame.time.get_ticks() - self.next_bullet >= 500 and self.shoot > 0:
                B2P1(1, True); B2P1(2, True); B2P1(3, True); B2P1(4, True)
                self.next_bullet = pygame.time.get_ticks()
                self.skill_cooldown = pygame.time.get_ticks()
                self.shoot -= 1
            
            if self.shoot <= 0:
                if pygame.time.get_ticks() - self.skill_cooldown >= 50:
                    self.shoot = 40
                    self.pattern = 2
                    self.bullet()
        
        if self.pattern == 2:
            if (pygame.time.get_ticks() - self.wait_skill_two >= 2000 and
                    not self.shoot_laser):
                self.first_bullet = B2P4(1)
                B2P4(2); B2P4(3); B2P4(4);
                self.next_bullet = pygame.time.get_ticks()
                self.shoot_laser = True
                 
            elif (pygame.time.get_ticks() - self.next_bullet >= 80 and
                    self.shoot_laser and not self.stop):
                self.last_bullet = B2P4(1)
                B2P4(2); B2P4(3); B2P4(4);
                self.next_bullet = pygame.time.get_ticks()
            
            if self.shoot_laser:
                if self.first_bullet.rect.y >= height or self.first_bullet.rect.y <= 0:
                    self.stop = True
                    if  self.last_bullet.rect.y >= height:
                        self.wait_skill_two = pygame.time.get_ticks()
                        self.next_bullet = pygame.time.get_ticks()
                        self.shoot = 20
                        self.shoot_laser = False
                        self.stop = False
                        self.pattern = 1
                        self.bullet()
                    

    def bullet(self):
        if self.pattern == 1:
            B2P1(1, True); B2P1(2, True); B2P1(3, True); B2P1(4, True)
            B2P2(1); B2P2(2)
            self.next_bullet = pygame.time.get_ticks()
        elif self.pattern == 2:
            B2P3(1); B2P3(2)
            self.wait_skill_two = pygame.time.get_ticks()

class B2P1(pygame.sprite.Sprite):

    def __init__(self, position, shoot=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['2'][0]
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.centerx = (curBoss.rect.centerx / 8) * 4
        elif position == 2:
            self.rect.centerx = (curBoss.rect.centerx / 8) * 5
        elif position == 3:
            self.rect.centerx = width - (curBoss.rect.centerx / 8) * 4
        elif position == 4:
            self.rect.centerx = width - (curBoss.rect.centerx / 8) * 5
        self.rect.y = curBoss.rect.bottom - 20
        self.radius = self.rect.width / 2 * 0.4
        self.hp = 5
        self.next_bullet = pygame.time.get_ticks()
        self.shoot = shoot
        self.speed = 4 + boss_difficult
        self.position = position

        all_sprites.add(self)
        boss_bullet.add(self)

    def update(self):
        self.rect.y += self.speed
# left gun and right gun
class B2P2(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['2'][1]
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.centerx = self.rect.width
            self.rect.y = curBoss.rect.bottom + 5
        elif position == 2:
            self.rect.centerx = width - (self.rect.width)
            self.rect.y = curBoss.rect.bottom + 120
            new_img = pygame.transform.rotate(self.image, 180)
            self.image = new_img
        self.radius = self.rect.width / 2 * 0.6
        self.hp = 15
        self.direction = 1
        self.position = position
        self.move_loop = 1
        self.speed = 2
        self.shoot_time = pygame.time.get_ticks()
        self.past_pos = self.rect.y
        self.stop = False
        
        all_sprites.add(self)
        boss_bullet.add(self)

        
    def update(self):
        # stop moving to shoot bullets
        if abs(self.rect.y - self.past_pos) >= 90:
            self.stop = True
            if self.position == 1:
                self.bullet = B2P2_bullet(self.rect.right + 10, self.rect.centery, self.position)
            elif self.position == 2:
                self.bullet = B2P2_bullet(self.rect.left - 10, self.rect.centery, self.position)
            self.past_pos = self.rect.y
            self.shoot_time = pygame.time.get_ticks()
        # shoot bullets while stop
        if self.stop:
            if pygame.time.get_ticks() - self.shoot_time >= 1500:
                self.stop = False
            else:
                if pygame.time.get_ticks() - self.bullet.delay >= 400:
                    if self.position == 1:
                        self.bullet = B2P2_bullet(self.rect.right + 13, self.rect.centery, self.position)
                    elif self.position == 2:
                        self.bullet = B2P2_bullet(self.rect.left - 13, self.rect.centery, self.position)
        # move the gun
        elif not self.stop:
            if self.direction == 1:
                self.rect.y += self.speed
            elif self.direction == 2:
                self.rect.y -= self.speed
        # move down and up and remove
        if self.move_loop > 0:
            if self.rect.y >= height - 10:
                self.direction = 2
                self.move_loop -= 1
            elif self.rect.y <= curBoss.rect.bottom + 5:
                self.direction = 1
                self.move_loop -= 1
        if self.move_loop < 0 or self.rect.y > height + 5 or self.rect.y <= curBoss.rect.bottom:
            self.kill()    
# bullets of gun
class B2P2_bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['2'][2]
        if direction in [3, 4]:
            new_img = pygame.transform.rotate(self.image, 90)
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = y
        else:
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
        self.radius = self.rect.width / 2 * 0.4
        self.direction = direction
        self.hp = 1
        self.speed = 3 + boss_difficult
        self.delay = pygame.time.get_ticks()

        all_sprites.add(self)
        boss_bullet.add(self)

    def update(self):
        if self.direction == 1:
            self.rect.x += self.speed
        elif self.direction == 2:
            self.rect.x -= self.speed
        elif self.direction == 3 or self.direction == 4:
            self.rect.y += self.speed
        if self.rect.x <= 0 or self.rect.x >= width:
            self.kill() 
# gun top left and right at pattern 2
class B2P3(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_boss_bullet['2'][1]
        new_img = pygame.transform.rotate(self.image, 270)
        self.image = new_img
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.centerx = width / 2  - (curBoss.rect.width / 2 + 60)
        elif position == 2:
            self.rect.centerx = width / 2  + (curBoss.rect.width / 2 + 60)
        self.rect.y = curBoss.rect.bottom - 80
        self.radius = self.rect.width / 2 * 0.6
        self.position = position
        self.hp = 15
        self.num_bullet = 10 # number of bullets at pattern 1
        self.bullet = B2P2_bullet(self.rect.centerx, self.rect.bottom + 7, self.position + 2)

        all_sprites.add(self)
        boss_bullet.add(self)
    
    def update(self):
        if pygame.time.get_ticks() - self.bullet.delay >= 400 and self.num_bullet > 0:
            self.bullet = B2P2_bullet(self.rect.centerx, self.rect.bottom + 7, self.position + 2)
            self.num_bullet -= 1

        if self.num_bullet <= 0:
            self.kill()
# laser beam
class B2P4(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        if position == 1:
            self.image = img_boss_bullet['2'][3]
            self.rect = self.image.get_rect()
            self.rect.centerx = width / 2 - 20
        elif position == 2:
            self.image = img_boss_bullet['2'][4]
            self.rect = self.image.get_rect() 
            self.rect.centerx = width / 2 - 60
        elif position == 3:
            self.image = img_boss_bullet['2'][3]
            self.rect = self.image.get_rect()
            self.rect.centerx = width / 2 + 20
        elif position == 4:
            self.image = img_boss_bullet['2'][4]
            self.rect = self.image.get_rect()
            self.rect.centerx = width / 2 + 60
        self.rect.y = curBoss.rect.bottom + 30
        self.radius = self.rect.width / 2 * 0.8
        self.position = position
        self.speed = 3 + boss_difficult
        self.change_direct = False

        all_sprites.add(self)
        boss_bullet.add(self)

    def update(self):
        # change direction of bullets
        if self.position in [1, 2]:
            if self.rect.centerx <= 100 and not self.change_direct:
                self.change_direct = True
            elif not self.change_direct:
                self.rect.x -= self.speed
                self.rect.y += 8
            else:
                self.rect.x += self.speed
                self.rect.y += 8
        elif self.position in [3, 4]:
            if self.rect.centerx >= width - 100 and not self.change_direct:
                self.change_direct = True
            elif not self.change_direct:
                self.rect.x += self.speed
                self.rect.y += 8
            else:
                self.rect.x -= self.speed
                self.rect.y += 8

        if self.rect.y >= height:
            self.kill()

#---------------------------- End Boss edit ---------------------------

# Sound
shoot_sound = pygame.mixer.Sound(path.join(snd_folder, 'laser_shoot.wav'))
expl_sound = pygame.mixer.Sound(path.join(snd_folder, 'explos.wav'))
pygame.mixer.music.load(path.join(snd_folder, 'bg.ogg'))
player_die_sound = pygame.mixer.Sound(path.join(snd_folder, 'die.wav'))
#------------------------------------------------------------------------
boss_appear_sound = pygame.mixer.Sound(
    path.join(snd_folder, 'boss_appearance.wav'))
#------------------------------------------------------------------------
pygame.mixer.music.set_volume(0.4)


pygame.mixer.music.play(loops=-1)

count = 3
game_over = True
running = True

#Boss-----------
hit_times = 0
boss_appear = False
phase = 65
bossOrder = 0
clone = 0
B2_baria = False
now = pygame.time.get_ticks()
#Boss-------------
def teleport():
    pass

while running:
    #print(count)
    if game_over:
        #print(count)
        main_menu(count)
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        mobbullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        #-------------------------------------
        boss_bullet = pygame.sprite.Group()
        boss_baria = pygame.sprite.Group()
        #-------------------------------------

        player = Player()
        all_sprites.add(player)

        for i in range(4):
            newmob()

        

        
        if count == 0:
            count = 3
            game_over_scr()
        score = 0

    

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in hits:
        #-----------------
        hit_times += 1
        #-----------------
        score += 50 - hit.radius
        expl_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)

        if random.random() > 0.95:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    #----------------------- Start ----------------------------
    # BOSS APPEARANCE !!
    if hit_times >= phase:
        hit_times = 0
        # mobs will be increased in each time when boss appear
        phase += phase * 0.3
        boss_appear = True

        for mob in mobs:
            mob.kill()
        expl.kill()
        pygame.mixer.music.load(path.join(snd_folder, 'boss_appearance.wav'))
        pygame.mixer.music.play(loops=-1)

        curBoss = BossCalling(bossOrder)
        all_sprites.add(curBoss)
        bg_color = 0
        while curBoss.rect.y <= width / 10:
            clock.tick(fps)
            curBoss.appear()
            bg_color += 1
            if bg_color <= 2:
                screen.fill(black)
            elif bg_color <= 3:
                screen.fill(pink_red)
            else:
                bg_color = 0
            all_sprites.draw(screen)
            draw_text(screen, 'Score: ' + str(score), 18, width / 2, 10)
            draw_text(screen, 'Lives: ' +
                      str(player.lives), 18, width - 45, 10)
            draw_hp_bar(screen, 5, 5, player.hp)
            pygame.display.flip()

        # at boss 2, add baria and control bullets by itself
        if bossOrder == 2:
            baria = Bossbaria()
            B2_baria = True
            curBoss.bullet()


    # hitting check
    if boss_appear:
        if bossOrder != 2:
            if len(boss_bullet) == 0 and pygame.time.get_ticks() - curBoss.skill_cooldown > 250:
                curBoss.bullet()
                curBoss.pattern += 1

        # check to see if a bullet hit boss
        hits = pygame.sprite.spritecollide(curBoss, bullets, True)
        for hit in hits:
            score += 100
            curBoss.hp -= hit.radius
            curBoss.image = img_boss_damaged[bossOrder]
            curBoss.image.set_colorkey(black)
            expl_sound.play()
            curBoss.hit_color_delay = pygame.time.get_ticks()

            if random.random() == 1:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)

        # color of boss
        if len(hits) == 0 and pygame.time.get_ticks() - curBoss.hit_color_delay >= 150:
            if bossOrder == 2:
                curBoss.image = img_boss[3]
            else:
                curBoss.image = img_boss[bossOrder]
        
        # if boss was killed call mobs change music
        if curBoss.hp <= 0:
            expl_sound.play()
            expl = Explosion(curBoss.rect.center, 'sulg')
            all_sprites.add(expl)
            curBoss.kill()
            boss_appear = False
            ############ if new boss is added already, delete if ##########
            # not delete this if, already make loop for boss 
            # if bossOrder == 0:
            #     bossOrder = 1
            # elif bossOrder == 1:
            #    bossOrder = 2
            # elif bossOrder == 2:
            #     bossOrder = 0

            bossOrder += 1
            if bossOrder == 3:
                bossOrder = 0
                boss_difficult += 2 #make boss harder after loop 
            for bullet in boss_bullet:
                bullet.kill()

            pygame.mixer.music.load(path.join(snd_folder, 'bg.ogg'))
            pygame.mixer.music.play(loops=-1)
            for i in range(5):
                newmob()

        # check to see if a bullet hit a boss_bullet
        hits = pygame.sprite.groupcollide(boss_bullet, bullets, False, True)
        for hit in hits:
            score += int(50 - hit.radius)
            try:
                hit.hp -= 1
                if hit.hp <= 0:
                    hit.kill()
            except:
                None
            expl_sound.play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)

            if random.random() > 0.9:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)

        # check to see if boss_bullet hit player
        hits = pygame.sprite.spritecollide(
            player, boss_bullet, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.hp -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)

            if player.hp <= 0:
                player_die_sound.play()
                death_explos = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explos)
                if player.lives < 0:
                    player.kill()
                player.hide()
                player.lives -= 1
                player.hp = 100
                count -= 1
                
                break

        # check to see if player collide with boss
        if pygame.sprite.collide_rect(curBoss, player):
            player.hp = 0
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)

            if player.hp <= 0:
                player_die_sound.play()
                death_explos = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explos)
                if player.lives < 0:
                    player.kill()
                player.hide()
                player.lives -= 1
                player.hp = 100
                count -= 1
                

        # check to see if player collide with baria
        if bossOrder == 2 and B2_baria:
            if baria.status:
                if pygame.sprite.collide_rect(baria, player):
                    player.hp = 0
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)

                    if player.hp <= 0:
                        player_die_sound.play()
                        death_explos = Explosion(player.rect.center, 'player')
                        all_sprites.add(death_explos)
                        if player.lives < 0:
                            player.kill()
                        player.hide()
                        player.lives -= 1
                        player.hp = 100
                        count -= 1
                        

                # check to see if a bullet hit boss baria
                hits = pygame.sprite.spritecollide(baria, bullets, True)
                for hit in hits:
                    score += 50
                    baria.hp -= hit.radius
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    expl_sound.play()

                    if random.random() == 1:
                        pow = Power(hit.rect.center)
                        all_sprites.add(pow)
                        powerups.add(pow)

    #------------------------ End ---------------------------

    # check to see if a mob hit player
    hits = pygame.sprite.spritecollide(
        player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.hp -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()

        if player.hp <= 0:
            player_die_sound.play()
            death_explos = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explos)
            #-----------------------------------------------
            if player.lives < 0:
                player.kill()
            player.hide()
            player.lives -= 1
            player.hp = 100
            count -= 1
            break
            #-----------------------------------------------

    # if player hit powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'hp':
            player.hp += random.randrange(30, 50)
            if player.hp >= 100:
                player.hp = 100
        if hit.type == 'gun':
            player.powerup()

    # check to see if a mob bullet hit player
    hits = pygame.sprite.spritecollide(
        player, mobbullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.hp -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)

        if player.hp <= 0:
            player_die_sound.play()
            death_explos = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explos)
            #-----------------------------------------------
            if player.lives < 0:
                player.kill()
            player.hide()
            player.lives -= 1
            player.hp = 100
            count -= 1
            break
            #-----------------------------------------------

    # if player died and explosion finish playing
    if player.lives <= 0 and not death_explos.alive():
        game_over = True
        #----------------------------------------------
        boss_appear = False
        for sprite in all_sprites:
            sprite.kill()

        #----------------------------------------------
        pygame.display.update()

    #----------------------------------------------------
    if boss_appear:
        bg_color += 1
        if bg_color <= 50:
            screen.fill(black)
        elif bg_color <= 55:
            screen.fill(pink_red)
        else:
            bg_color = 0
    else:
        screen.fill(black)
    #----------------------------------------------------

    #screen.blit(bg, bg_rect)
    #bg
    for star in stars_bg_list1:
        

        pygame.draw.rect(screen, (255, 255, 255), (star[0], star[1], 1,1), 0)
        star[1] = star[1] + 1
        if star[1] > height :
            star[1] = -10
            star[0] = random.randint(0, width)
    
    for star in stars_bg_list2:
        pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), 2, 0)
        star[1] = star[1] + 2
        if star[1] > height :
            star[1] = -10
            star[0] = random.randint(0, width)
        

    all_sprites.draw(screen)

    draw_text(screen, 'Score: ' + str(score), 25, width / 2, 2)
    draw_text(screen, 'Lives: ' + str(player.lives), 25, width - 45, 2)
    draw_hp_bar(screen, 5, 5, player.hp)



    pygame.display.flip()


pygame.quit()
