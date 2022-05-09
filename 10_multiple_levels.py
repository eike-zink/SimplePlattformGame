import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHRACTER_SCALING = 1.0
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

GRAVITY = 1.0

# Movement speed of player
PLAYER_MOVEMENT_SPEED = 5.0
PLAYER_JUMP_SEED = 20.0
# Player start position
PLAYER_START_X = 64
PLAYER_START_Y = 255

# Layer Names from our TileMap
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Don't Touch"

class MyGame(arcade.Window):
    """Main application class"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # TileMap Object
        self.tile_map = None
        # Our Scene Object
        self.scene = None
        # Where is the right edge of the map?
        self.end_of_map = 0
        # Level
        self.level = 1
        # Separate variable that holds the player sprite
        self.player_sprite = None
        # Load sounds
        self.player_collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.player_jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        # Our physics engine
        self.physics_engine = None
        # A Camera that can be used for scrolling the screen
        self.camera = None
        # A Camera that can be used to draw GUI element on the screen
        self.gui_camera = None
        # Keep track of the score
        self.score = 0
        # Set background color
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
    def setup(self):
        """Set up the game. Call this function to restart the game"""
        # TileMap
        # Name of map file to load
        map_name = f":resources:tiled_maps/map2_level_{self.level}.json"
        # Options for the layer
        map_layer_options = {
            LAYER_NAME_PLATFORMS: {"use_spatial_hash": True},
            LAYER_NAME_COINS: {"use_spatial_hash": True},
            LAYER_NAME_DONT_TOUCH: {"use_spatial_hash": True}
        }
        # Read tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, map_layer_options)
        # Initialize Scene and background
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # Keep track of the score
        self.score = 0
        # Set the bckground  color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        # Set up the player
        image_source = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHRACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        # Add Player Spritelist before "Foreground"
        self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND)
        self.scene.add_sprite("Player", self.player_sprite)
        # Calculate the right edge of the map
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        # Create the physic engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        # Set up the Score
        self.score = 0

    def on_draw(self):
        """Render the screen"""
        # Clear the screen to the background color
        self.clear()
        # Activate the camera
        self.camera.use()
        # Draw our Scene
        self.scene.draw()
        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()
        # Draw score on the screen
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key: int, modifiers: int):
        """Called whenever a key is pressed"""
        if key == arcade.key.UP and self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SEED
            arcade.play_sound(self.player_jump_sound)
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
        # See if the player hit any coins
        coins = arcade.check_for_collision_with_list(
            sprite=self.player_sprite,
            sprite_list=self.scene["Coins"]
        )
        # Loop through each coin the player hit and remove it
        for coin in coins:
            # Add one to the score
            self.score += 1
            # Remove the coin
            coin.remove_from_sprite_lists()
            # and play a sound
            arcade.play_sound(self.player_collect_coin_sound)
        # Did the player fall of the map?
        if self.player_sprite.center_x < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            arcade.play_sound(self.game_over)
        # Did the player toud something they should not?
        if arcade.check_for_collision_with_list(
            sprite=self.player_sprite,
            sprite_list=self.scene[LAYER_NAME_DONT_TOUCH]
        ):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            arcade.play_sound(self.game_over)
        # See it the user got the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1
            # Load the next level
            self.setup()
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