from settings import *
from engine import Engine

class App:
    rl.init_window(WIN_WIDTH, WIN_HEIGHT, 'Aurora BSP')

    def __init__(self):
        self.dt = 0.0   # Delta Time
        self.engine = Engine(app = self)

    def run(self):
        while not rl.window_should_close():
            self.dt = rl.get_frame_time()
            self.engine.update()
            self.engine.draw()
        #
        rl.close_window()


if __name__ == '__main__':
    app = App()
    app.run()

