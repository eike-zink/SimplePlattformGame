import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHRACTER_SCALING = 1.0
TILE_SCALING = 0.5

class MyGame(arcade.Window):
    """Main application class"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # These are lists that keep track of our sprites. Each sprite should go into a list
        self.wall_list = None
        self.player_list = None
        # Separate variable that holds the player sprite
        self.player_sprite = None
        # Set background color
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
    def setup(self):
        """Set up the game. Call this function to restart the game"""
        # Create the Sprite lists
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList()
        # Set up the player
        image_source = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHRACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)
        # Create the ground 
        image_source = ":resources:images/tiles/grassMid.png"
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(image_source, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        # Put some crates on the ground
        image_source = ":resources:images/tiles/boxCrate_double.png"
        coordinate_list = [[512, 96], [256, 96], [786, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(image_source, TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

    def on_draw(self):
        """Render the screen"""

        # Clear the screen to the background color
        self.clear()
        # Draw the sprites
        self.wall_list.draw()
        self.player_list.draw()


def main():
    game = MyGame()
    game.setup()
    game.run()


if __name__ == '__main__':
    main()