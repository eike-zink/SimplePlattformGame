import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHRACTER_SCALING = 1.0
TILE_SCALING = 0.5

GRAVITY = 1.0

# Movement speed of player
PLAYER_MOVEMENT_SPEED = 5.0
PLAYER_JUMP_SEED = 20.0

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
        # A Camera that can be used for scrolling the screen
        self.camera = None
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
        # Put some boxes on the ground
        image_source = ":resources:images/tiles/boxCrate_double.png"
        coordinate_list = [[512, 96], [256, 96], [786, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(image_source, TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
        # Create the physic engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene.get_sprite_list("Walls")
        )
        # Set uo the Camera
        self.camera = arcade.Camera(self.width, self.height)

    def on_draw(self):
        """Render the screen"""
        # Clear the screen to the background color
        self.clear()
        # Draw the sprites
        self.scene.draw()
        # Activate the camera
        self.camera.use()

    def on_key_press(self, key: int, modifiers: int):
        """Called whenever a key is pressed"""
        if key == arcade.key.UP and self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key: int, modifiers: int):
        """Called when the user release a key"""
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):
        """Movemonet and game logic"""
        # Move the player with the physics engine
        self.physics_engine.update()
        # Position the camera
        self._center_camera_to_player()

    def _center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        # Stopp camera at 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

        

def main():
    game = MyGame()
    game.setup()
    game.run()


if __name__ == '__main__':
    main()