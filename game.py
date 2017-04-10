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

# Set up folder
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
            self.speedx = -6
        if keystate[pygame.K_RIGHT]:
            self.speedx = 6
        self.rect.x += self.speedx

        if keystate[pygame.K_DOWN]:
            self.speedy = 6
        if keystate[pygame.K_UP]:
            self.speedy = -6
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
        self.init_pos = [100, 150, 200, 200, 250,
                         245, 250, 300, 300, 350, 400]
        self.image_orig = random.choice(meteor_img)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.choice(self.init_pos)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = 0
        self.speedy = random.randrange(4, 7)
        self.rot = 0
        #self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

   # def rotate(self):
        # now = pygame.time.get_ticks()
        # if now - self.last_update > 50:
        #     self.last_update = now
        #     self.rot = (self.rot + self.rot_speed) % 360
        #     new_img = pygame.transform.rotate(self.image_orig, self.rot)
        #     old_center = self.rect.center
        #     self.image = new_img
        #     self.rect = self.image.get_rect()
        #     self.rect.center = old_center

    def update(self):
        # self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(4, 7)


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


class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        #------------------------------------------------
        self.radius = self.rect.w / 2 * 0.8
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


def show_go_screen(x):
    if x != 0:
        #screen.blit(bg, bg_rect)
        draw_text(screen, 'Space Shooter', 80, width / 2, height / 4)
        draw_text(screen, 'Arrow keys to move, Space to fire',
                  30, width / 2, height / 2)
        draw_text(screen, 'Press any key to begin',
                  30, width / 2, height * 3 / 4)
    else:
        #screen.blit(bg, bg_rect)
        draw_text(screen, 'Game Over', 64, width / 2, height / 2)

    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False


# Graphic
#bg = pygame.image.load(path.join(img_folder, 'menu.jpg')).convert()
#bg_rect = bg.get_rect()

player_img = pygame.image.load(path.join(img_folder, 'plane.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
bullet_img = pygame.image.load(path.join(img_folder, 'laserRed.png')).convert()

meteor_img = []
meteor_list = ['m1.png', 'm2.png', 'm3.png',
               'm4.png', 'm5.png', 'm6.png', 'm7.png', 'm8.png']
for img in meteor_list:
    meteor_img.append(pygame.image.load(path.join(img_folder, img)).convert())

explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
#--------------Boss------------------
explosion_animation['sulg'] = []
#--------------Boss------------------
explosion_animation['player'] = []
for i in range(9):
    filename = 'e{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
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
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(black)
    explosion_animation['player'].append(img)

powerup_img = {}
powerup_img['hp'] = pygame.image.load(
    path.join(img_folder, 'hp.png')).convert()
powerup_img['gun'] = pygame.image.load(
    path.join(img_folder, 'gun.png')).convert()

#--------------------------- Start Boss edit --------------------------

img_boss = []
img_boss_damaged = []
img_boss_bullet = {}
for i in range(2):
    img_boss_bullet[str(i)] = []

for i in range(2):
    filename = 'b{}.png'.format(i)
    image = pygame.image.load(path.join(img_folder, filename)).convert()
    img_boss.append(image)

    filename = 'bd{}.png'.format(i)
    image = pygame.image.load(path.join(img_folder, filename)).convert()
    img_boss_damaged.append(image)

    filename = 'bb{}.png'.format(i)
    image = pygame.image.load(path.join(img_folder, filename)).convert()
    img_boss_bullet[str(i)].append(image)
    if i == 1:
        image = pygame.image.load(path.join(img_folder, 'bb10.png')).convert()
        img_boss_bullet['1'].append(image)


def BossCalling(order):
    if order == 0:
        return Boss_0()
    elif order == 1:
        return Boss_1()


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
                expl = Explosion(self.rect.center, 'sm')
                all_sprites.add(expl)
                boss_bullet.add(expl)
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
phase = 100
bossOrder = 0
clone = 0
now = pygame.time.get_ticks()
#Boss-------------

#star bg
stars_bg_list = [[random.randint(0, width), random.randint(0, height)] for x in range(200)]

while running:
    

    if game_over:
        show_go_screen(count)
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        #-------------------------------------
        boss_bullet = pygame.sprite.Group()
        #-------------------------------------

        player = Player()
        all_sprites.add(player)

        for i in range(7):
            newmob()

        score = 0

    clock.tick(fps)

    #bg
    for star in stars_bg_list:
        pygame.draw.line(screen, (255, 255, 255), (star[0], star[1]), (star[0], star[1]))
    star[0] = star[0] - 1
    if star[0] < 0:
        star[0] = width
        star[1] = random.randint(0, height)

    pygame.display.update()

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

        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    #----------------------- Start ----------------------------
    # BOSS APPEARANCE !!
    if hit_times >= phase:
        hit_times = 0
        phase *= (1.5)
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

    # hitting check
    if boss_appear:
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
            curBoss.image = img_boss[bossOrder]

        # if boss was killed call mobs change music
        if curBoss.hp <= 0:
            curBoss.kill()
            boss_appear = False
            ############ if new boss is added already, delete if ##########
            # not delete this if, already make loop for boss 
            if bossOrder == 0:
                bossOrder = 1
            elif bossOrder == 1:
                bossOrder = 0
                boss_difficult += 2 #make boss harder after loop 
            for bullet in boss_bullet:
                bullet.kill()

            pygame.mixer.music.load(path.join(snd_folder, 'bg.ogg'))
            pygame.mixer.music.play(loops=-1)
            for i in range(9):
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
            player.hp += random.randrange(10, 30)
            if player.hp >= 100:
                player.hp = 100
        if hit.type == 'gun':
            player.powerup()

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

    all_sprites.draw(screen)

    draw_text(screen, 'Score: ' + str(score), 18, width / 2, 10)
    draw_text(screen, 'Lives: ' + str(player.lives), 18, width - 45, 10)
    draw_hp_bar(screen, 5, 5, player.hp)

    pygame.display.flip()


pygame.quit()
