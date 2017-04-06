# Art from kenney in opengameart.org
# Sound from Jan125 in opengameart.org

import pygame
import random
from os import path

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
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx

        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        self.rect.y += self.speedy

        if keystate[pygame.K_SPACE]:
            self.shoot()

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
        self.rect.bottom = height + 200


class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_img)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(50, 430)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = 0
        self.speedy = random.randrange(6, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

   # def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_img = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        #self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Power(pygame.sprite.Sprite):

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['hp','gun'])
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
        draw_text(screen, 'Arrow keys to move, Space to fire', 30, width / 2, height / 2)
        draw_text(screen, 'Press any key to begin', 30, width / 2, height * 3 / 4)
    else:
        #screen.blit(bg, bg_rect)
        draw_text(screen, 'Game Over', 64, width / 2, height / 2)

    pygame.display.update()
    waiting = True
    while  waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                waiting = False
   
    




# Graphic
#bg = pygame.image.load(path.join(img_folder, 'menu.jpg')).convert()
#bg_rect = bg.get_rect()

player_img = pygame.image.load(path.join(img_folder, 'plane.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
bullet_img = pygame.image.load(path.join(img_folder, 'laserRed.png')).convert()

meteor_img = []
meteor_list = ['m1.png']
for img in meteor_list:
    meteor_img.append(pygame.image.load(path.join(img_folder, img)).convert())

explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
explosion_animation['player'] = []
for i in range(9):
    filename = 'e{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animation['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animation['sm'].append(img_sm)

    filename = 'sx{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(black)
    explosion_animation['player'].append(img)

powerup_img = {}
powerup_img['hp'] = pygame.image.load(path.join(img_folder, 'hp.png')).convert()
powerup_img['gun'] = pygame.image.load(path.join(img_folder, 'gun.png')).convert()


# Sound
shoot_sound = pygame.mixer.Sound(path.join(snd_folder, 'laser_shoot.wav'))
expl_sound = pygame.mixer.Sound(path.join(snd_folder, 'explos.wav'))
pygame.mixer.music.load(path.join(snd_folder, 'bg.ogg'))
player_die_sound = pygame.mixer.Sound(path.join(snd_folder, 'die.wav'))
pygame.mixer.music.set_volume(0.4)


pygame.mixer.music.play(loops=-1)

count = 3
game_over = True
running = True
while running:
    if game_over:
        show_go_screen(count)
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        for i in range(9):
            newmob()

        score = 0

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in hits:
        score += 50 - hit.radius
        expl_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

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
            player.hide()
            player.lives -= 1
            player.hp = 100
            count -= 1
    
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
        pygame.display.update()
        

    screen.fill(black)
    #screen.blit(bg, bg_rect)

    all_sprites.draw(screen)

    draw_text(screen, 'Score: ' + str(score), 18, width / 2, 10)
    draw_text(screen, 'Lives: ' + str(player.lives), 18, width - 45, 10)
    draw_hp_bar(screen, 5, 5, player.hp)

    pygame.display.flip()
    

pygame.quit()
