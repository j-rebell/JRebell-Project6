import arcade
import random
import sys

class Galaga(arcade.Window):
    def __init__(self):
        super().__init__(800, 1600, "Galaga Clone")
        self.ship = None
        self.enemies = arcade.SpriteList()
        self.shots = arcade.SpriteList()
        self.shot_sound = None
        self.ship_dx = 0
        self.enemies_dy = 0
        self.score = 0
        self.lives = 3
        self.lives_counter = arcade.SpriteList()
        self.enemy_speed = .5
        self.shot_speed = 5
        self.music = None
    def setup(self):
        self.ship = arcade.Sprite("ship8up.png")
        self.shot_sound = arcade.load_sound(":resources:sounds/laser2.wav")
        self.ship.center_x = 400
        self.ship.center_y = 64
        self.music = arcade.load_sound("E1M1.wav")
        for num in range(6):
            enemy = arcade.Sprite("Enemy.png")
            enemy.center_x = random.randint(64, 736)
            enemy.center_y = random.randint(1200, 1600)
            self.enemies.append(enemy)
        for num in range(self.lives):
            life = arcade.Sprite("ship8up.png", .25)
            life.center_x = len(self.lives_counter) * 16 + 16
            life.center_y = 16
            self.lives_counter.append(life)
    def on_draw(self):
        arcade.start_render()
        self.ship.draw()
        self.enemies.draw()
        self.shots.draw()
        self.lives_counter.draw()
        arcade.finish_render()
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.ship_dx = -4
        elif symbol == arcade.key.RIGHT:
            self.ship_dx = 4
        if symbol == arcade.key.SPACE:
            if len(self.shots) < 5:
                shot = arcade.Sprite("shot.png")
                shot.center_x = self.ship.center_x
                shot.center_y = self.ship.center_y
                self.shots.append(shot)
                arcade.play_sound(self.shot_sound)
            else:
                pass
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.ship_dx = 0
    def on_update(self, delta_time: float):
        if self.score >= 20:
            arcade.play_sound(self.music)
        self.ship.center_x += self.ship_dx
        if self.ship.center_x <= 64 or self.ship.center_x >= 736:
            self.ship_dx = 0
        for enemy in self.enemies:
            enemy.center_y += -self.enemy_speed
        for shot in self.shots:
            shot.center_y += self.shot_speed
            if shot.center_y > 1632:
                self.shots.remove(shot)
            enemy_death = arcade.check_for_collision_with_list(shot, self.enemies)
            if enemy_death:
                for enemy in enemy_death:
                    self.enemies.remove(enemy)
                    self.score += 1
                    self.shots.remove(shot)
                    new_enemy = arcade.Sprite("Enemy.png")
                    new_enemy.center_x = random.randint(64, 736)
                    new_enemy.center_y = random.randint(1600, 2000)
                    self.enemies.append(new_enemy)
        life_lost = arcade.check_for_collision_with_list(self.ship, self.enemies)
        if life_lost:
            for enemy in life_lost:
                self.lives -= 1
                for life in self.lives_counter[-1]:
                    self.lives_counter.remove(life)
                self.enemies.remove(enemy)

