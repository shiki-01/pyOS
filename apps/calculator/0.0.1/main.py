import pyxel

class App:
    def __init__(self):
        self.expression = ""
        self.buttons = [
            ('7', 10, 10), ('8', 40, 10), ('9', 70, 10), ('/', 100, 10),
            ('4', 10, 30), ('5', 40, 30), ('6', 70, 30), ('*', 100, 30),
            ('1', 10, 50), ('2', 40, 50), ('3', 70, 50), ('-', 100, 50),
            ('0', 10, 70), ('C', 40, 70), ('=', 70, 70), ('+', 100, 70)
        ]
        pyxel.run(self.updatee, self.draw)

    def updatee(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for button, x, y in self.buttons:
                if x <= pyxel.mouse_x <= x + 20 and y <= pyxel.mouse_y <= y + 15:
                    self.on_button_click(button)

    def on_button_click(self, button):
        if button == 'C':
            self.expression = ""
        elif button == '=':
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = "Error"
        else:
            self.expression += button

    def draw(self):
        pyxel.rect(0, 0, 160, 120, 1)
        pyxel.text(5, 5, self.expression, 7)
        for button, x, y in self.buttons:
            pyxel.rect(x, y, 20, 15, 9)
            pyxel.text(x+5, y+4, button, 7)
