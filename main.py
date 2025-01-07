import sys
import threading
import time

import core.logging
import game.loader
from core.texture import TextureLoader
from core.game import SceneKonsoleBuffer, GameLoader
from core.input import InputHandler
from core import Vec2, util
from core.updating import UpdateHandler

def epilepsy_warn():
    for i in range(20):
        print("EPILEPSY WARNING")
        time.sleep(0.25)

    proceed = input("Proceed with game (Y/N): ")
    if not (proceed.lower() == "y" or proceed.lower() == "yes"):
        print("Epilepsy Ending!")
        sys.exit(0)

def main():
    print("Starting game...")
    print("Loading textures...")
    #Load textures from res/texture
    TextureLoader.load()

    print("Registering Loaders...")
    #register game loaders
    game.loader.register_loader()

    threading.current_thread().name = "Render"

    #Instantiate Buffer
    print("Creating render buffer...")
    buffer = SceneKonsoleBuffer(Vec2(200, 50))
    core.util.buffer = buffer
    buffer.disable_fps_cap()
    #buffer.set_fps_target(1)
    #Create InputHandler instance
    print("Instantiating input handler...")
    InputHandler(buffer)
    print("Instantiating update handler...")
    UpdateHandler(buffer)
    #Invoke GameLoader#on_make_buffer(gamelib.SceneKonsoleBuffer) for all registered loaders
    print("Instantiating game...")
    GameLoader.invoke_on_make_buffer(buffer)

    epilepsy_warn()

    #Main game loop
    print("Launching update loop...")
    UpdateHandler.instance.launch()
    try:
        while not buffer.should_quit():
            GameLoader.invoke_pre_frame(buffer)
            buffer.flush()
    except KeyboardInterrupt:
        print("Closing...")
        UpdateHandler.instance.quit()
        UpdateHandler.instance.join()
        core.logging.force_flush()
        print("Closed")

    print(core.util.ending)


main()