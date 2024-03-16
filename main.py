import arcade
import math

# задаем ширину, высоту и заголовок окна

SCREEN_TITLE = "Bomberman"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800


class Animate(arcade.Sprite):
    i = 0
    time = 0

    def update_animation(self, delta_time):  # Swaps between textures based on delta_time
        self.time += delta_time
        if self.time >= 0.1:
            self.time = 0
            if self.textures:
                self.i = (self.i + 1) % len(self.textures)
                self.set_texture(self.i)


class Tank:
    class Base(arcade.Sprite):
        def __init__(self):
            super().__init__("Tank/Base1.png", 2.5)
            self.setup()

            self.SPEED = 2
            self.TURN_SPEED = 1
            self.change_angle = self.TURN_SPEED

            self.move_dir = ""
            self.turn_dir = ""

        def move(self):
            if self.move_dir == "forward":
                self.calculate_move_dir()
                self.center_x += self.change_x
                self.center_y += self.change_y
            if self.move_dir == "back":
                self.calculate_move_dir()
                self.center_x -= self.change_x
                self.center_y -= self.change_y
            else:
                self.change_y = 0
                self.change_x = 0

        def calculate_move_dir(self):
            self.change_x = self.SPEED * math.cos(math.radians(self.angle))
            self.change_y = self.SPEED * math.sin(math.radians(self.angle))

        def turn(self):
            if self.turn_dir == "right":
                self.angle -= self.change_angle
            if self.turn_dir == "left":
                self.angle += self.change_angle
            else:
                self.TURN_SPEED = 0

        def update(self):
            # __Move function__
            self.move()
            self.turn()

        def setup(self):
            # __Start position__
            self.center_x = SCREEN_WIDTH / 2
            self.center_y = SCREEN_HEIGHT / 2

            # __Start Angle__
            self.angle = 100

    class Tower(Animate):
        def __init__(self):
            super().__init__("Tank/Tower1.png", 2.5)
            self.setup()
            """Textures"""
            self.frames_shoot = [arcade.load_texture("Tank/Tower2.png"),
                                 arcade.load_texture("Tank/Tower3.png"),
                                 arcade.load_texture("Tank/Tower4.png"),
                                 arcade.load_texture("Tank/Tower5.png")]

            """Angle"""
            self.TURN_SPEED = 1
            self.change_angle = self.TURN_SPEED
            self.rotate_dir = ""

            self.is_shooting = False
            self.shoot_timer = 0
            self.shoot_duration = 0.30

        def shoot(self):
            if not self.is_shooting:
                self.textures = self.frames_shoot
                self.is_shooting = True
                self.shoot_timer = 0
                arcade.play_sound(window.shoot_sound, volume=0.1)

        def rotate(self):
            if self.rotate_dir == "right":
                self.angle -= self.change_angle
            if self.rotate_dir == "left":
                self.angle += self.change_angle
            else:
                self.TURN_SPEED = 0

        def reset_texture(self):
            self.textures = [arcade.load_texture("Tank/Tower1.png")]
            self.is_shooting = False

        def setup(self):
            pass

        def update(self, delta_time):
            # __Be on the same cord as Base__
            self.center_x = window.base.center_x
            self.center_y = window.base.center_y

            self.rotate()

            if self.is_shooting:
                self.shoot_timer += delta_time
                if self.shoot_timer >= self.shoot_duration:
                    self.reset_texture()


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # текстуры
        # self.bg = arcade.load_texture('Blocks/BackgroundTile.png')

        self.setup()

        """Sprites"""
        self.tank = Tank()
        self.base = self.tank.Base()
        self.tower = self.tank.Tower()

        """Sounds"""
        self.shoot_sound = arcade.load_sound("Tank/Shoot.WAV", 0.1)

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        """Sprites"""
        self.base.draw()
        self.tower.draw()

    def update(self, delta_time):

        """Sprites"""
        self.tower.update(delta_time)
        self.tower.update_animation(delta_time)
        self.base.update()

    def on_key_press(self, key, modifiers):
        # __Tower Inputs__
        if key == arcade.key.E:
            self.tower.rotate_dir = "right"
        if key == arcade.key.Q:
            self.tower.rotate_dir = "left"
        if key == arcade.key.SPACE:
            self.tower.shoot()

        # __Base Inputs__
        if key == arcade.key.W:
            self.base.move_dir = "forward"
        if key == arcade.key.S:
            self.base.move_dir = "back"
        if key == arcade.key.D:
            self.base.turn_dir = "right"
        if key == arcade.key.A:
            self.base.turn_dir = "left"

    def on_key_release(self, key, modifiers):
        # __Tower Inputs__
        if key == arcade.key.E:
            self.tower.rotate_dir = ""
        if key == arcade.key.Q:
            self.tower.rotate_dir = ""

        # __Base Inputs__
        if key == arcade.key.W:
            self.base.move_dir = ""
        if key == arcade.key.S:
            self.base.move_dir = ""
        if key == arcade.key.D:
            self.base.turn_dir = ""
        if key == arcade.key.A:
            self.base.turn_dir = ""


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
