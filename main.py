"""
Platformer Game
"""
import arcade

# Constants

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"
# Constant for movement and speed of player
PLAYER_MOVEMENT_SPEED = 5

# Constants used to scale sprites
CHARACTER_SCALING = 1
TITLE_SCALING = 0.5

# Constant for gravity and jump speed
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# Add Coins and sound
COIN_SCALING = 0.5

class MyGame(arcade.Window):
    """
    Main application class
    """
    # Init
    def __init__(self):
        # Call parent class and setup window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Scene Object
        self.scene = None

        # separate variable that holds player sprite
        self.player_sprite = None
        
        # Camera for scrolling the screen
        self.camera = None
                
                
        # Our physics engine
        self.physics_engine = None
        
        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        
        # Camera used to draw GUI elements
        self.gui_camera =None
        
        # Score tracking
        self.score = 0
        
        # Color for background
        arcade.set_background_color(arcade.color.EBONY)

    # Setup function
    def setup(self):
        """setup game here. call this function to restart the game"""

        # Seup Camera
        self.camera = arcade.Camera(self.width, self.height)
        
        # Initialize Scene
        self.scene = arcade.Scene()
        
        # Create sprite list here
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, placing at its coordinates
        image_source = ":resources:images/animated_characters/female_Adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # create the ground
        # shows using loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TITLE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinates_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinates_list:
            # add a crate on the ground
            wall = arcade.Sprite(""
                                 ":resources:images/tiles/boxCrate_double.png", TITLE_SCALING
                                 )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )
        
        # Loop to place coins for character interaction
        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            coin.center_x = x 
            coin.center_y = 96
            self.scene.add_sprite("Coins", coin)
        
        # Setuo the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)
        
        # Score tracking
        self.score = 0
        
    # on_draw    
    def on_draw(self):
        """Render the screen"""

        # Clear the screen to the background color
        arcade.start_render()

        # Activate our Camera
        self.camera.use()
        
        # Code to draw the sprites here
        self.scene.draw()
        
        # Activate GUI before drawing GUI elements
        self.gui_camera.use()
        
        # Draw score to screen, scrolling w/viewport
        score_text = f"Score:{self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18, 
        )
        
               
    # key down and key up event handlers       
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
                
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key"""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
            
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
            
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
            
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
    
    # Center camera to player
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        
        self.camera.move_to(player_centered)
        
    # On Update
    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()
        
        # Position the camera
        self.center_camera_to_player()
        
        # Coin collision detection
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )
        
        # Loop through each coin, if we hit any remove it
        for coin in coin_hit_list:
            # Remove coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
