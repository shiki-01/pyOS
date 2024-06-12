import pyxel, os, shutil, datetime

class VirtualOS:
    def __init__(self, working_dir="os_files"):
        self.working_dir = working_dir
        os.makedirs(self.working_dir, exist_ok=True)
        self.path = os.getcwd()
        self.files = os.listdir(self.working_dir)
        self.selected = 0

    def create_file(self, filename, content=""):
        with open(os.path.join(self.working_dir, filename), "w") as file:
            file.write(content)

    def read_file(self, filename):
        with open(os.path.join(self.working_dir, filename), "r") as file:
            return file.read()

    def write_file(self, filename, content):
        with open(os.path.join(self.working_dir, filename), "w") as file:
            file.write(content)

    def delete_file(self, filename):
        os.remove(os.path.join(self.working_dir, filename))

    def update(self):
        # ここにキーボード入力に応じたファイル操作のロジックを追加
        pass

    def draw(self):
        pyxel.text(0, 0, self.path, 7)
        for i, file in enumerate(self.files):
            if i == self.selected:
                pyxel.rect(0, 10 + i * 7, 160, 10 + i * 7 + 7, 1)
            pyxel.text(0, 10 + i * 7, file, 7)

class App:
    def __init__(self):
        pyxel.init(320, 240, title="Hello Pyxel")
        pyxel.load("assets/main.pyxres")
        pyxel.mouse(True)
        self.virtual_os = VirtualOS()
        self.menu_open = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.virtual_os.update()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            if 5 <= x <= 21 and pyxel.height - 16 <= y <= pyxel.height:
                self.toggle_menu()

    def toggle_menu(self):
        self.menu_open = not self.menu_open

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        self.virtual_os.draw()
        self.draw_bottom_bar()
        if self.menu_open:
            self.draw_menu()

    def draw_bottom_bar(self):
        bar_height = 16
        pyxel.rect(0, pyxel.height - bar_height, pyxel.width, bar_height, 1)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        pyxel.text(pyxel.width - 35, pyxel.height - (bar_height / 2) - (5 / 2), current_time, 7)
        pyxel.blt(5, pyxel.height - (bar_height / 2) - (16 / 2), 0, 16, 0, 16, 16, 0)

    def draw_menu(self):
        menu_height = 200
        pyxel.rect((pyxel.width / 2) - (200 / 2), pyxel.height - menu_height, 200, menu_height, 9)

if __name__ == "__main__":
    App()