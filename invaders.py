import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, KEYDOWN, KEYUP
from random import randint

WIDTH = 640
HEIGHT = 480

class Game:
    def __init__(self):
        self.aliens = self.make_aliens()
        self.player = Player(self)
        self.alien_bullets = []
        self.player_bullets = []
        self.game_over = False

    def make_aliens(self):
        return [Alien(self, x*30, y*30) for x in range(10) for y in range(6)]

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
            alien.shoot_maybe()
        for bullet in self.alien_bullets:
            bullet.move()
        for bullet in self.player_bullets:
            bullet.move()
        self.alien_bullets = filter(lambda b : b.y < 480, self.alien_bullets)
        self.player_bullets = filter(lambda b : b.y >= 0, self.player_bullets)
        self.set_alien_direction()

    def detect_collisions(self):
        for bullet in self.player_bullets:
            for alien in self.aliens:
                if abs(bullet.x - alien.x) < 10 and abs(bullet.y - alien.y) < 10:
                    alien.alive = False
        self.aliens = filter(lambda alien : alien.alive, self.aliens)

        for bullet in self.alien_bullets:
            if bullet.x == self.player.x and bullet.y == self.player.y:
                self.player.lives -= 1
                if self.player.lives < 0:
                    self.game_over = True
                else:
                    self.player.x = WIDTH / 2

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
        if randint(0, 1000) == 1:
            self.game.alien_bullets.append(Bullet(self.x, self.y, 1))

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
        self.y = 440
        self.game = game
        self.img = pygame.image.load("player.png")
        self.rect = self.img.get_rect()
        self.speed = 0

    def accel(self, direction):
        if direction == 1:
            self.speed = 4
        elif direction == -1:
            self.speed = -4
        else:
            self.speed = 0

    def move(self):
        self.x += self.speed
        if self.x < 10:
            self.x = 10
        elif self.x > 610:
            self.x = 610

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
            self.y += 20
        else:
            self.y -= 20

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
                main_surface.blit(alien.img, (alien.x, alien.y))
            for bullet in game.player_bullets:
                main_surface.blit(bullet.img, (bullet.x, bullet.y))
            for bullet in game.alien_bullets:
                main_surface.blit(bullet.img, (bullet.x, bullet.y))

            main_surface.blit(game.player.img, (game.player.x, game.player.y))
            pygame.display.flip()

            game.player.move()
            if timer % 100 == 0:
                game.update_all()
            timer += 1

    pygame.quit()


main()
