import game.loader
from core.texture import TextureLoader
from core.game import SceneKonsoleBuffer, GameLoader
from core.input import InputHandler
from core import Vec2
from core.updating import UpdateHandler

def main():
    #Load textures from res/texture
    TextureLoader.load()

    #register game loaders
    game.loader.register_loader()

    #Instantiate Buffer
    buffer = SceneKonsoleBuffer(Vec2(200, 50))
    buffer.disable_fps_cap()
    #buffer.set_fps_target(1)
    #Create InputHandler instance
    InputHandler(buffer)
    UpdateHandler(buffer)
    #Invoke GameLoader#on_make_buffer(gamelib.SceneKonsoleBuffer) for all registered loaders
    GameLoader.invoke_on_make_buffer(buffer)

    #Main game loop
    UpdateHandler.instance.launch()
    try:
        while not buffer.should_quit():
            GameLoader.invoke_pre_frame(buffer)
            buffer.flush()
    except KeyboardInterrupt:
        print("Closing...")
        UpdateHandler.instance.quit()
        UpdateHandler.instance.join()
        print("Closed")

if __name__ == '__main__':
    main()
