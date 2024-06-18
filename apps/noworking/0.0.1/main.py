import pyxel

class App:
    def __init__(self):
        self.window_x = 10
        self.window_y = 10
        self.window_width = 150
        self.window_height = 100
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    def draw(self):
        pyxel.rect(self.window_x, self.window_y, self.window_width, self.window_height, 9)
        pyxel.text(self.window_x + 4, self.window_y + 4, "no working", 7)

if __name__ == "__main__":
    App()