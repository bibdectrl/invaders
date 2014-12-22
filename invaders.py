import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, KEYDOWN, KEYUP
from random import randint

WIDTH = 64
HEIGHT = 48

class Game:
    def __init__(self):
        self.aliens = self.make_aliens()
        self.player = Player(self)
        self.alien_bullets = []
        self.player_bullets = []
        self.game_over = False

    def make_aliens(self):
        return [Alien(self, x*3, y*3) for x in range(10) for y in range(6)]

    def set_alien_direction(self):
        # aliens have hit the right side of the screen, so they switch directions to move down
        if len(filter(lambda a : a.x >= WIDTH and a.direction == 1, self.aliens)) > 0:
            for alien in self.aliens:
                alien.direction = 10
        # aliens have moved down on the right side of the screen, so they switch directions to move left
        elif len(filter(lambda a : a.x >= WIDTH and a.direction == 10, self.aliens)) > 0:
            for alien in self.aliens:
                alien.direction = -1
        # aliens have hit the left side of the screen, so they switch directions to move down
        elif len(filter(lambda a : a.x <= 0 and a.direction == -1, self.aliens)) > 0:
            for alien in self.aliens:
                alien.direction = 10
        # aliens have moved down on the left side of the screen, so they switch directions to move right
        elif len(filter(lambda a : a.x <= 0 and a.direction == 10, self.aliens)) > 0:
            for alien in self.aliens:
                alien.direction = 1                

    def update_all(self):
        self.detect_collisions()
        for alien in self.aliens:
            alien.move()
        for bullet in self.alien_bullets:
            bullet.move()
        for bullet in self.player_bullets:
            bullet.move()
#        self.alien_bullets = filter(lambda b : b < HEIGHT and b >= 0, self.alien_bullets)
        self.player_bullets = filter(lambda b : b.y >= 0, self.player_bullets)
        self.set_alien_direction()

    def detect_collisions(self):
        for bullet in self.player_bullets:
            for alien in self.aliens:
                if bullet.x == alien.x and bullet.y == alien.y:
                    alien.alive = False
        self.aliens = filter(lambda alien : alien.alive, self.aliens)

        for bullet in self.alien_bullets:
            if bullet.x == player.x and bullet.y == player.y:
                self.player.lives -= 1
                if player.lives < 0:
                    self.game_over = True
                else:
                    player.x = WIDTH / 2

class Alien:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.direction = 1
        self.alive = True
        self.img = pygame.image.load("alien.png")
        self.rect = self.img.get_rect()

    def shoot_maybe(self):
        if randint(10) == 1:
            game.bullets.append(Bullet(self.x, self.y, 1))

    def __str__(self):
        return "Alien at " + str(self.x) + ", " + str(self.y)

    def move(self):
        if self.direction == 1:
            self.x += 1
        elif self.direction == -1:
            self.x -= 1
        elif self.direction == 10:
            self.y += 1

    def set_image(img):
        self.img = img

class Player:
    def __init__(self, game):
        self.x = WIDTH / 2
        self.y = 460
        self.game = game
        self.img = pygame.image.load("player.png")
        self.rect = self.img.get_rect()
        self.speed = 0

    def accel(self, direction):
        if direction == 1:
            self.speed = 4
        elif direction == -1:
            self.speed = -4

    def move(self):
        self.x += self.speed

    def shoot(self):
        if len(self.game.player_bullets) < 5:
            self.game.player_bullets.append(Bullet(self.x, self.y, -1))

    def set_image(img):
        self.img = img

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.img = pygame.image.load("bullet.png")
        self.rect = self.img.get_rect()

    def set_image(img):
        self.img = img

    def move(self):
        if self.direction == 1:
            self.y += 10
        else:
            self.y -= 10

def main():
    pygame.init()
    main_surface = pygame.display.set_mode((640, 480))
    game = Game()
    timer = 0
    while True:
        if game.game_over:
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
        else:
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            if ev.type == KEYDOWN:
                if ev.key == K_LEFT:
                    game.player.accel(-1)
                elif ev.key == K_RIGHT:
                    game.player.accel(1)
                elif ev.key == K_SPACE:
                    game.player.shoot()
                elif ev.key == K_ESCAPE:
                    break
            if ev.type == KEYUP:
                if ev.key == K_LEFT:
                    game.player.speed = 0
                elif ev.key == K_RIGHT:
                    game.player.speed = 0


            main_surface.fill((0, 0, 0, 0))
            for alien in game.aliens:
                main_surface.blit(alien.img, (alien.x * 10, alien.y * 10))
            for bullet in game.player_bullets:
                main_surface.blit(bullet.img, (bullet.x, bullet.y))
            for bullet in game.alien_bullets:
                main_surface.blit(bullet.img, (bullet.x * 10, bullet.y * 10))

            main_surface.blit(game.player.img, (game.player.x, 460))
            pygame.display.flip()

            game.player.move()
            if timer % 100 == 0:
                game.update_all()
            timer += 1

    pygame.quit()


main()
