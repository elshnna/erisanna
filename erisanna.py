import pyxel
import random
import math

pyxel.init(256, 256)

class Background:
    def __init__(self):
        self.time = 0
        self.time_enemy = 30

class Player:
    def __init__(self):
        self.x = 90
        self.y = 200
        self.vx = 2
        self.vy = 2
        self.alive = True

class Bullet_Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = -5
        self.alive = True

class Enemy:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.bullets_frequency = 45
        self.alive = True

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x <= 241:
            self.vx = -self.vx
        if self.x >= 0:
            self.vx = -self.vx

class Bullet_Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 3
        self.alive = True

class Game:
    def __init__(self):
        self.background = Background()
        self.player = Player()
        self.bullets_player = []
        self.enemies = []
        self.bullets_enemies = []
        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_background()
        self.update_player()
        self.update_bullets_player()
        self.update_enemies()
        self.update_bulletes_enemies()
        self.update_enemy_to_bullets_player()
        self.update_player_to_bullets_enemies()
        self.update_bullets_player_to_bullets_enemies()
        self.update_player_to_enemies()

    def update_background(self):
        if self.player.alive:
            self.background.time += 1

    def update_player(self):
        if pyxel.btn(pyxel.KEY_W):
            self.player.y -= self.player.vy
        if pyxel.btn(pyxel.KEY_A):
            self.player.x -= self.player.vx
        if pyxel.btn(pyxel.KEY_S):
            self.player.y += self.player.vy
        if pyxel.btn(pyxel.KEY_D):
            self.player.x += self.player.vx
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bullets_player.append(Bullet_Player(self.player.x + 6, self.player.y + 1))

    def update_bullets_player(self):
        for b in self.bullets_player:
            b.x += b.vx
            b.y += b.vy

    def update_enemies(self):
        angle = 0

        if self.background.time_enemy > 0:
            self.background.time_enemy -= 1

        if 0 < self.background.time_enemy <= 1:
            angle = pyxel.rndi(30, 150)
            self.enemies.append(Enemy(pyxel.rndi(0, 240), 0, random.uniform(-1, 1), 0.5))

        if self.background.time_enemy <= 0:
            self.background.time_enemy += 450 / math.sqrt(self.background.time)

        for b in self.enemies:
            if b.alive == 1:
                b.move()
            if b.bullets_frequency > 0:
                b.bullets_frequency -= 1
            else:
                b.bullets_frequency += 30

    def update_bulletes_enemies(self):
        for b in self.enemies:
            if b.bullets_frequency == 0:
                self.bullets_enemies.append(Bullet_Enemy(b.x + 6, b.y + 1))
        for b in self.bullets_enemies:
            b.x += b.vx
            b.y += b.vy

    def update_player_to_enemies(self):
        for b in self.enemies:
            if -15 <= b.x - self.player.x <= 15 and -15 <= b.y - self.player.y <= 15:
                self.player.alive = False
                b.alive = False

    def update_player_to_bullets_enemies(self):
        for b in self.bullets_enemies:
            if 0 <= b.x - self.player.x <= 15 and 0 <= b.y - self.player.y <= 15:
                self.player.alive = False
                b.alive = False

    def update_enemy_to_bullets_player(self):
        for b in self.enemies:
            for c in self.bullets_player:
                if 0 <= c.x - b.x <= 15 and 0 <= b.y - c.y <= 15:
                    b.alive = False
                    c.alive = False

    def update_bullets_player_to_bullets_enemies(self):
        for b in self.bullets_enemies:
            for c in self.bullets_player:
                if -2 <= b.x - c.x <= 2 and -2 <= c.y - b.y <= 2:
                    b.alive = False
                    c.alive = False

    def draw(self):
        pyxel.cls(0)
        if self.player.alive:
            pyxel.rect(self.player.x, self.player.y, 15, 15, 2)
        else:
            pyxel.text(95, 112, "YOUR SCORE:" + str(self.background.time), 8)

        for b in self.bullets_player:
            if b.alive:
                pyxel.rect(b.x, b.y, 3, 3, 3)

        for b in self.enemies:
            if b.alive:
                pyxel.rect(b.x, b.y, 15, 15, 5)

        for b in self.bullets_enemies:
            if b.alive:
                pyxel.rect(b.x, b.y, 3, 3, 5)

Game()
