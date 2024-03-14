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
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
                self.set_texture(self.i)


class Tank:
    class Base(arcade.Sprite):
        def __init__(self):
            super().__init__("Tank/Base1.png", 2.5)
            self.setup()
            self.speed = 4

        def setup(self):
            # __Start position__
            self.center_x = SCREEN_WIDTH / 2
            self.center_y = SCREEN_HEIGHT / 2

            # __Start Angle__
            self.angle = 0

        def move(self, direction, mode):
            if mode:
                if direction == "forward":
                    self.change_x = self.speed * math.cos(math.radians(self.angle))
                    self.change_y = self.speed * math.sin(math.radians(self.angle))
                elif direction == "back":
                    self.change_x = -self.speed * math.cos(math.radians(self.angle))
                    self.change_y = -self.speed * math.sin(math.radians(self.angle))
            else:
                self.change_x = 0
                self.change_y = 0

        def update(self):
            self.center_x += self.change_x
            self.center_y += self.change_y

    class Tower(Animate):
        def __init__(self):
            super().__init__("Tank/Tower1.png", 2.5)
            self.setup()

            """Angle"""
            self.TURN_SPEED = 1

        def setup(self):
            pass

        def update(self):
            # __Be on the same cord as Base__
            self.center_x = window.base.center_x
            self.center_y = window.base.center_y

            # __ChangeAngle__
            self.angle += self.change_angle

        # __Turn functions__
        def turning(self, direction, mode):
            if mode:
                if direction == "right":
                    self.change_angle = -self.TURN_SPEED
                elif direction == "left":
                    self.change_angle = self.TURN_SPEED
            else:
                self.change_angle = 0


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

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        """Sprites"""
        self.base.draw()
        self.tower.draw()

    def update(self, delta_time):

        """Sprites"""
        self.tower.update()
        self.base.update()

    def on_key_press(self, key, modifiers):
        # __Tower Inputs__
        if key == arcade.key.E:
            self.tower.turning("right", True)

        if key == arcade.key.Q:
            self.tower.turning("left", True)

        # __Base Inputs__
        if key == arcade.key.W:
            self.base.move("forward", True)

        if key == arcade.key.S:
            self.base.move("back", True)

    def on_key_release(self, key, modifiers):
        # __Tower Inputs__
        if key == arcade.key.E:
            self.tower.turning("right", False)

        if key == arcade.key.Q:
            self.tower.turning("left", False)

        # __Base Inputs__
        if key == arcade.key.W:
            self.base.move("forward", False)

        if key == arcade.key.S:
            self.base.move("back", False)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
