import pyxel, os, shutil, datetime, importlib.util, threading
from packaging.version import parse


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
        pyxel.text(0, 10, "Click on the application menu from the logo in the bottom right-hand corner,", 7)
        pyxel.text(0, 15, "towards the version name, to launch it.", 7)
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
        self.selected_app = None
        self.selected_app_position = (0, 0)
        self.dragging = False
        self.window_x = 50
        self.window_y = 50
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.running_app_instance = None
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.running_app_instance and hasattr(self.running_app_instance, 'update'):
            self.running_app_instance.update()
        else:
            # 通常のupdateロジック
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            self.virtual_os.update()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                x, y = pyxel.mouse_x, pyxel.mouse_y
                if 5 <= x <= 21 and pyxel.height - 16 <= y <= pyxel.height:
                    self.toggle_menu()
                self.check_app_selection(pyxel.mouse_x, pyxel.mouse_y)
                if self.selected_app:
                    self.run_selected_app()
                    self.selected_app = None
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if self.window_x <= mx <= self.window_x + 160 and self.window_y <= my <= self.window_y + 20:
                self.dragging = True
                self.drag_offset_x = mx - self.window_x
                self.drag_offset_y = my - self.window_y
            elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.dragging = False
            if self.dragging:
                self.window_x = pyxel.mouse_x - self.drag_offset_x
                self.window_y = pyxel.mouse_y - self.drag_offset_y

    def toggle_menu(self):
        self.menu_open = not self.menu_open

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        self.virtual_os.draw()
        self.draw_bottom_bar()
        if self.menu_open:
            self.draw_menu()
        if self.selected_app:
            self.draw_pseudo_window()
            pyxel.rect(self.window_x, self.window_y, 160, 120, 13)
            pyxel.rect(self.window_x, self.window_y, 160, 20, 7)

    def draw_bottom_bar(self):
        bar_height = 16
        pyxel.rect(0, pyxel.height - bar_height, pyxel.width, bar_height, 1)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        pyxel.text(pyxel.width - 35, pyxel.height - (bar_height / 2) - (5 / 2), current_time, 7)
        pyxel.blt(5, pyxel.height - (bar_height / 2) - (16 / 2), 0, 16, 0, 16, 16, 0)

    def get_latest_apps(self):
        apps_dir = 'apps'
        latest_apps = []
        for app_name in os.listdir(apps_dir):
            app_path = os.path.join(apps_dir, app_name)
            if os.path.isdir(app_path):
                versions = [d for d in os.listdir(app_path) if os.path.isdir(os.path.join(app_path, d))]
                latest_version = max(versions, key=parse)
                latest_apps.append((app_name, latest_version))
        return latest_apps

    def draw_menu(self):
        menu_width = 160
        menu_height = 120
        menu_x = (pyxel.width / 2) - (menu_width / 2)
        menu_y = (pyxel.height / 2) - (menu_height / 2)
        pyxel.rect(menu_x, menu_y, menu_width, menu_height, 1)
        pyxel.rectb(menu_x, menu_y, menu_width, menu_height, 7)
        latest_apps = self.get_latest_apps()
        for i, (app_name, version) in enumerate(latest_apps):
            pyxel.text(menu_x + 5, menu_y + 5 + i * 7, f"{app_name} {version}", 7)

    def check_app_selection(self, x, y):
        menu_x, menu_y = self.get_menu_position()
        latest_apps = self.get_latest_apps()
        for i, (app_name, version) in enumerate(latest_apps):
            if menu_x < x < menu_x + 160 and menu_y + 5 + i * 7 < y < menu_y + 12 + i * 7:
                self.selected_app = (app_name, version)
                break
    
    def draw_pseudo_window(self):
        menu_x, menu_y = self.get_menu_position()
        pyxel.rect(menu_x, menu_y, 160, 120, 13)
        latest_apps = self.get_latest_apps()
        for i, (app_name, version) in enumerate(latest_apps):
            pyxel.text(menu_x + 5, menu_y + 5 + i * 7, f"{app_name} {version}", 7)

    def selected_app_window(self, module):
        module.App()

    def run_selected_app(self):
        if self.selected_app is None:
            return

        def run_app():
            app_name, version = self.selected_app
            app_path = os.path.join('apps', app_name, version)
            spec = importlib.util.spec_from_file_location("app", os.path.join(app_path, "main.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            app_instance = module.App()
            while hasattr(app_instance, 'update'):
                app_instance.update()
                app_instance.draw()

        app_thread = threading.Thread(target=run_app)
        app_thread.start()
        self.selected_app = None

    def get_menu_position(self):
        menu_width = 160
        menu_height = 120
        menu_x = (pyxel.width / 2) - (menu_width / 2)
        menu_y = (pyxel.height / 2) - (menu_height / 2)
        return menu_x, menu_y

if __name__ == "__main__":
    App()