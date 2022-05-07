import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHRACTER_SCALING = 1.0
TILE_SCALING = 0.5

# Movement speed of player
PLAYER_MOVEMENT_SPEED = 5.0

class MyGame(arcade.Window):
    """Main application class"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Our Scene Object
        self.scene = None
        # Separate variable that holds the player sprite
        self.player_sprite = None
        # Our physics engine
        self.physics_engine = None
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
        # Create the physic engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            player_sprite=self.player_sprite,
            walls=self.scene.get_sprite_list("Walls")
        )

    def on_draw(self):
        """Render the screen"""
        # Clear the screen to the background color
        self.clear()
        # Draw the sprites
        self.scene.draw()

    def on_key_press(self, key: int, modifiers: int):
        """Called whenever a key is pressed"""
        if key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key: int, modifiers: int):
        """Called when the user release a key"""
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):
        """Movemonet and game logic"""
        # Move the player with the physics engine
        self.physics_engine.update()

        

def main():
    game = MyGame()
    game.setup()
    game.run()


if __name__ == '__main__':
    main()