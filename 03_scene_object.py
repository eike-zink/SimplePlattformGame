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
        # Our Scene Object
        self.scene = None
        # Separate variable that holds the player sprite
        self.player_sprite = None
        # Set background color
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
    def setup(self):
        """Set up the game. Call this function to restart the game"""
        # Initialize Scene
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        # Set up the player
        image_source = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHRACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        # Create the ground 
        image_source = ":resources:images/tiles/grassMid.png"
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(image_source, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)
        # Put some crates on the ground
        image_source = ":resources:images/tiles/boxCrate_double.png"
        coordinate_list = [[512, 96], [256, 96], [786, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(image_source, TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

    def on_draw(self):
        """Render the screen"""

        # Clear the screen to the background color
        self.clear()
        # Draw the sprites
        self.scene.draw()


def main():
    game = MyGame()
    game.setup()
    game.run()


if __name__ == '__main__':
    main()