import arcade
import random
import time

class Galaga(arcade.Window):
    def __init__(self):
        super().__init__(800, 1600, "Galaga Clone")
        self.ship = None
        self.enemies = arcade.SpriteList()
        self.shots = arcade.SpriteList()
        self.shot_sound = None
        self.score_sound = None
        self.ship_dx = 0
        self.enemies_dy = 0
        self.score = 0
        self.score_text = None
        self.lives = 3
        #Implimented a 3 life system drawn on the bottom left of the screen
        self.lives_counter = arcade.SpriteList()
        self.enemy_speed = 1
        self.shot_speed = 5
        self.music = None
        self.game_over = None
        self.won = None
        self.music_counter = 0
        self.music_playing = None
        self.win_counter = 0
        #Everyhting I currently need to make the game work at a basic level
    def setup(self):
        #Ship came from the zip file. Self music ended up being unused as arcade is not happy to play any version of the file I give, mp3 or wav even in mono
        self.ship = arcade.Sprite("ship8up.png")
        self.shot_sound = arcade.load_sound(":resources:sounds/laser2.wav")
        self.score_sound = arcade.load_sound(":resources:sounds/jump3.wav")
        self.ship.center_x = 400
        self.ship.center_y = 64
        self.music = arcade.load_sound("E1M1.wav")
        self.game_over = arcade.Text("Game Over", 400, 800, arcade.color.RED, 50)
        #Initial drawing of enemies
        for num in range(6):
            enemy = arcade.Sprite("Enemy.png")
            enemy.center_x = random.randint(64, 736)
            enemy.center_y = random.randint(1200, 1600)
            self.enemies.append(enemy)
        #Life counters are handled as a sprite list also
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
        #Setting up the game over screen
        if self.lives < 1:
            self.game_over.draw()
        self.score_text = arcade.Text(f"{int(self.score * 1000)}", 736, 16, arcade.color.WHITE, 16)
        self.score_text.draw()
        #Telling the player they won
        if self.score >= 20:
            self.won = arcade.Text(f"You won!\nYour score was, {int(self.score * 1000)}", 16, 800, arcade.color.GREEN, 25)
            self.won.draw()
            self.win_counter += 1
        arcade.finish_render()
        #Pyhton did not enjoy sleeping during the render. I'm sure there is a cleaner way to handle this but it works.

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.ship_dx = -5
        elif symbol == arcade.key.RIGHT:
            self.ship_dx = 5
        if symbol == arcade.key.SPACE:
            if len(self.shots) < 5:
                shot = arcade.Sprite("shot.png")
                shot.center_x = self.ship.center_x
                shot.center_y = self.ship.center_y
                self.shots.append(shot)
                arcade.play_sound(self.shot_sound)
            else:
                pass
        #These are some bindings to make testing easier. The program does not seem to recognise game over but will do game won when using the cheater keys.
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.U:
            self.score += 1
        if symbol == arcade.key.I:
            self.score -= 1
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.ship_dx = 0
    def on_update(self, delta_time: float):
        #Again not used but left in for attempts in the future
        if self.score >= 10 and self.music_counter == 0:
            self.enemy_speed *= 4
            self.music_playing = arcade.play_sound(self.music)
            self.music_counter += 1
            arcade.set_background_color(arcade.color.MAROON)
        #Handling player borders. Not elegant and can be overcome but works well enough
        self.ship.center_x += self.ship_dx
        if self.ship.center_x <= 64 or self.ship.center_x >= 736:
            self.ship_dx = 0
        #Used to make the enemies move towards the player
        for enemy in self.enemies:
            enemy.center_y += -self.enemy_speed
            if enemy.center_y <0:
                self.enemies.remove(enemy)
                new_enemy = arcade.Sprite("Enemy.png")
                new_enemy.center_x = random.randint(64, 736)
                new_enemy.center_y = random.randint(1600, 2000)
                self.enemies.append(new_enemy)
                self.score -= .5
        #Sprite list to control the laser sprite list. Speed can easily be changed for fine tuning.
        for shot in self.shots:
            shot.center_y += self.shot_speed
            if shot.center_y > 1632:
                self.shots.remove(shot)
            #Handling when the player kills an enemy
            enemy_death = arcade.check_for_collision_with_list(shot, self.enemies)
            if enemy_death:
                for enemy in enemy_death:
                    arcade.play_sound(self.score_sound)
                    self.enemies.remove(enemy)
                    self.score += 1
                    self.shots.remove(shot)
                    new_enemy = arcade.Sprite("Enemy.png")
                    new_enemy.center_x = random.randint(64, 736)
                    new_enemy.center_y = random.randint(1600, 2000)
                    self.enemies.append(new_enemy)
                    print(self.score)
        #Finding out whether to subtract a life from the player
        life_lost = arcade.check_for_collision_with_list(self.ship, self.enemies)
        if life_lost:
            rem_life_x = int(self.lives * 16)
            #Removing the sprite caused a lot of frustration as get sprites at point would not return anyhting
            get_life = arcade.get_sprites_at_point([rem_life_x, 16], self.lives_counter)
            rem_life = get_life[-1]
            for enemy in life_lost:
                self.lives -= 1
                self.enemies.remove(enemy)
                self.lives_counter.remove(rem_life)
                new_enemy = arcade.Sprite("Enemy.png")
                new_enemy.center_x = random.randint(64, 736)
                new_enemy.center_y = random.randint(1600, 2000)
                self.enemies.append(new_enemy)
        #Closing the window after a loss
        if self.lives < 1:
            time.sleep(5)
            arcade.close_window()
        if self.win_counter > 0:
            arcade.stop_sound(self.music_playing)
            time.sleep(5)
            arcade.close_window()

