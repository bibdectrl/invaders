import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, KEYDOWN, KEYUP
from random import randint

WIDTH = 640
HEIGHT = 480
SHIP_SIZE = 32
BULLET_SIZE = 4

class Game:
    def __init__(self):
        self.aliens = self.make_aliens()
        self.aliens.reverse()
        self.player = Player(self)
        self.alien_bullets = []
        self.player_bullets = []
        self.game_over = False
        self.game_won = False

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
        if self.player.dead:
            self.player.dead = False
        if len(self.aliens) == 0:
            self.game_won = True
            self.game_over = True    
        self.aliens = filter(lambda alien : alien.alive, self.aliens)
        self.detect_collisions()
        for alien in self.aliens:
            alien.move()
            alien.shoot_maybe()
        for bullet in self.alien_bullets:
            bullet.move()
        for bullet in self.player_bullets:
            bullet.move()
        self.alien_bullets = filter(lambda b : b.y < 480 and b.active, self.alien_bullets)
        self.player_bullets = filter(lambda b : b.y >= 0 and b.active, self.player_bullets)
        self.set_alien_direction()

    def detect_collisions(self):
        for bullet in self.player_bullets:
            for alien in self.aliens:
                if bullet.active and abs((bullet.x + BULLET_SIZE/2) - (alien.x + SHIP_SIZE/2)) < SHIP_SIZE/2 and abs((bullet.y+BULLET_SIZE/2) - (alien.y+SHIP_SIZE/2)) < SHIP_SIZE/2:
                    alien.alive = False
                    bullet.active = False
        self.aliens = sorted(self.aliens, key = lambda a : -a.y)
        self.alien_bullets = filter(lambda bullet : bullet.active, self.alien_bullets)

        for bullet in self.alien_bullets:
            if bullet.active and abs((bullet.x + BULLET_SIZE/2) - (self.player.x + SHIP_SIZE/2)) < SHIP_SIZE/2 and abs((bullet.y + BULLET_SIZE/2) - (self.player.y + SHIP_SIZE/2)) < SHIP_SIZE/2:
                self.player.dead = True
                bullet.active = False
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
        self.exploded = pygame.image.load("alien_dies.png")
        self.rect = self.img.get_rect()

    def shoot_maybe(self):
        if randint(0, len(self.game.aliens * 60)) == 1:
            self.game.alien_bullets.append(Bullet(self.x, self.y, 1))

    def __str__(self):
        return "Alien at " + str(self.x) + ", " + str(self.y)

    def move(self):
        if self.direction == 1:
            self.x += 2
        elif self.direction == -1:
            self.x -= 2
        elif self.direction == 10:
            self.y += 2

    def set_image(img):
        self.img = img

class Player:
    def __init__(self, game):
        self.x = WIDTH / 2
        self.y = 440
        self.game = game
        self.img = pygame.image.load("player.png")
        self.exploded = pygame.image.load("player_dies.png")
        self.rect = self.img.get_rect()
        self.speed = 0
        self.lives = 3
        self.dead = False

    def accel(self, direction):
        if direction == 1:
            self.speed = 3
        elif direction == -1:
            self.speed = -3
        elif direction == 0:
            self.speed = 0

    def move(self):
        self.x += self.speed
        if self.x < 10:
            self.x = 10
        elif self.x > 610:
            self.x = 610

    def shoot(self):
        if len(self.game.player_bullets) < 5:
            self.game.player_bullets.append(Bullet(self.x + 13, self.y + 15, -1))

    def set_image(img):
        self.img = img

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.img = pygame.image.load("bullet.png")
        self.rect = self.img.get_rect()
        self.active = True

    def set_image(img):
        self.img = img

    def move(self):
        if self.direction == 1:
            self.y += 10
        else:
            self.y -= 10

def main():
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 15)
    main_surface = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Shitty Space Invaders")
    game = Game()
    timer = pygame.time.Clock()
    game_over = myfont.render("Game Over! (press space to restart)", 1, (255, 255, 0))
    game_won = myfont.render("You Win! (press space to restart)", 1, (255, 255, 0))

    while True:
        timer.tick(60)
        if game.game_over:
            main_surface.fill((0, 0, 0, 0))
            if game.game_won:
                main_surface.blit(game_won, (100, 100))
            else:
                main_surface.blit(game_over, (100, 100))
            pygame.display.flip()
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            if ev.type == KEYDOWN:
                if ev.key == K_SPACE:
                    game = Game()
                    game.game_over = False
                    game.game_won = False
                elif ev.key == K_ESCAPE:
                    break
  
        else:
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break

            if ev.type == KEYUP:
                if ev.key == K_LEFT or ev.key == K_RIGHT:
                    game.player.speed = 0

            if ev.type == KEYDOWN:
                if ev.key == K_LEFT:
                    game.player.accel(-1)
                if ev.key == K_RIGHT:
                    game.player.accel(1)
                if ev.key == K_SPACE:
                    game.player.shoot()
                if ev.key == K_ESCAPE:
                    break

            main_surface.fill((0, 0, 0, 0))
            for alien in game.aliens:
                if alien.alive:
                    main_surface.blit(alien.img, (alien.x, alien.y))
                else:
                    main_surface.blit(alien.exploded, (alien.x, alien.y))
            for bullet in game.player_bullets:
                if bullet.active:
                    main_surface.blit(bullet.img, (bullet.x, bullet.y))
            for bullet in game.alien_bullets:
                main_surface.blit(bullet.img, (bullet.x, bullet.y))


            if game.player.dead:
                main_surface.blit(game.player.exploded, (game.player.x, game.player.y))
            else:
                main_surface.blit(game.player.img, (game.player.x, game.player.y))
            lives = myfont.render("Lives: " + str(game.player.lives), 1, (255, 255, 0))
            main_surface.blit(lives, (20, 400))
            pygame.display.flip()

            game.player.move()
            game.update_all()

    pygame.quit()


main()
