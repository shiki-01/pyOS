import pyxel, os, shutil

class VirtualOS:
    def __init__(self):
        self.path = "C:/"
        self.files = os.listdir(self.path)
        self.selected = 0
        self.selected_file = self.files[self.selected]
        self.selected_file_path = self.path + self.selected_file

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.files) - 1
            self.selected_file = self.files[self.selected]
            self.selected_file_path = self.path + self.selected_file
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selected += 1
            if self.selected >= len(self.files):
                self.selected = 0
            self.selected_file = self.files[self.selected]
            self.selected_file_path = self.path + self.selected_file
        if pyxel.btnp(pyxel.KEY_END):
            if os.path.isdir(self.selected_file_path):
                self.path = self.selected_file_path + "/"
                self.files = os.listdir(self.path)
                self.selected = 0
                self.selected_file = self.files[self.selected]
                self.selected_file_path = self.path + self.selected_file
            else:
                shutil.copy(self.selected_file_path, "C:/Desktop/")
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.path = "/".join(self.path.split("/")[:-2]) + "/"
            self.files = os.listdir(self.path)
            self.selected = 0
            self.selected_file = self.files[self.selected]
            self.selected_file_path = self.path + self.selected_file

    def draw(self):
        pyxel.rect(0, 0, 160, 10, 1)
        pyxel.text(0, 0, self.path, 7)
        for i, file in enumerate(self.files):
            if i == self.selected:
                pyxel.rect(0, 10 + i * 7, 160, 10 + i * 7 + 7, 1)
            pyxel.text(0, 10 + i * 7, file, 7)


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.load("assets/main.pyxres")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        VirtualOS().update()
        VirtualOS().draw()

    def mouse(self):
        x = pyxel.mouse_x
        y = pyxel.mouse_y
        pyxel.blt(x, y, 0, 0, 0, 16, 16, 0)

App()
VirtualOS()