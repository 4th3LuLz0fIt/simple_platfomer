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


class MyGame(arcade.Window):
    """
    Main application class
    """

    def __init__(self):
        # Call parent class and setup window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Scene Object
        self.scene = None

        # separate variable that holds player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None
        
        # Camera for scrolling the screen
        

        # Color for background
        arcade.set_background_color(arcade.color.EBONY)

    def setup(self):
        """setup game here. call this function to restart the game"""

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

    def on_draw(self):
        """Render the screen"""

        # Clear the screen to the background color
        arcade.start_render()

        # Code to draw the sprites here
        self.scene.draw()
        
    # key down and key up event handlers       
    def on_key_press_draw(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
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

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
