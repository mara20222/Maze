from pygame import *

width = 700
height = 500
window = display.set_mode((700,500))
display.set_caption('лабиринт(хелп)')

background = transform.scale(image.load('background.jpg'),(700,500))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, p_x, p_y, p_speed):
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def run(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < height - 80:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def run(self):
        if self.rect.x <= 500:
            self.direction = 'right'
        if self.rect.x >= width - 40:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, c1, c2, c3, w_x, w_y, width, height):
        super().__init__()
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill((c1,c2,c3))
        self.rect = self.image.get_rect()
        self.rect.x = w_x
        self.rect.y = w_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


hero = Player('hero.png', 5, height - 80, 5)
enemy = Enemy('cyborg.png', width - 80, 280, 5)
gold = GameSprite('treasure.png', width - 120, height - 80, 0)

w1 = Wall(46, 58, 222, 100, 20, 450, 10)
w2 = Wall(46, 58, 222, 100, 480, 350, 10)
w3 = Wall(46, 58, 222, 100, 20, 10, 380)
w4 = Wall(46, 58, 222, 200, 150, 10, 330)
w5 = Wall(46, 58, 222, 300, 20, 10, 380)
w6 = Wall(46, 58, 222, 450, 150, 10, 340)
w7 = Wall(46, 58, 222, 400, 150, 150, 10)


game = True
finish = False
FPS = 60
clock = time.Clock()

font.init()
font = font.SysFont('Arial', 40)
win = font.render('Молодец, через 20 секунд все твои учетные записи удалятся, а компьютер отключится', True, (0,0,0))
lose = font.render('Молодец, через 20 секунд все твои учетные записи удалятся, а компьютер отключится', True, (0,0,0))

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background,(0,0))
        hero.reset()
        enemy.reset()
        gold.reset()

        hero.run()
        enemy.run()

        w1.reset()
        w2.reset()
        w3.reset()
        w4.reset()
        w5.reset()
        w6.reset()
        w7.reset()

    if sprite.collide_rect(hero, gold):
        finish = True
        window.blit(win, (40,200))
        money.play()

    if sprite.collide_rect(hero, enemy) or sprite.collide_rect(hero, w1) or sprite.collide_rect(hero, w2) or sprite.collide_rect(hero, w3) or sprite.collide_rect(hero, w4) or sprite.collide_rect(hero, w5) or sprite.collide_rect(hero, w6) or sprite.collide_rect(hero, w7):
        finish = True
        window.blit(lose, (40, 200))
        kick.play()

    display.update()
    clock.tick(FPS)