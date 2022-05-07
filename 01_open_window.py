import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

class MyGame(arcade.Window):
    """Main application class"""

    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game. Call this function to restart the game"""
        pass

    def on_draw(self):
        """Render the screen"""
        self.clear()
        # Code to draw the screen goes here


def main():
    game = MyGame()
    game.setup()
    game.run()


if __name__ == '__main__':
    main()