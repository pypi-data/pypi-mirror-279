import tkinter as tk

class OnScreenNumpad(tk.Tk):
    def __init__(self):
        super().__init__()

        self.value = None

        self.title("On-Screen Numpad")
        self.geometry("300x300")

        self.tf = tk.Entry(self)
        self.tf.pack()
        self.tf.config(width=40)

        self.label = tk.Label(self, text="")
        self.label.pack()

        self.button_clear = tk.Button(self, text="Clear", command=self.clear_text)
        self.button_clear.pack()

        # On-screen keyboard
        self.keyboard = tk.Frame(self)
        self.keyboard.pack()

        key_layout = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["ENTER"]]

        for row_idx, row in enumerate(key_layout):
            for col_idx, key in enumerate(row):
                button = self.create_keyboard_button(key)
                button.grid(row=row_idx, column=col_idx, padx=2, pady=2)

        #self.made_by_label = tk.Label(self, text="Made by ElliNet13")
        #self.made_by_label.pack()
                
class OnScreenCustom(tk.Tk):
    def __init__(self, name, key_layout, size):
        super().__init__()

        self.value = None

        self.title("On-Screen " + name)
        self.geometry(size)

        self.tf = tk.Entry(self)
        self.tf.pack()
        self.tf.config(width=40)

        self.label = tk.Label(self, text="")
        self.label.pack()

        self.button_clear = tk.Button(self, text="Clear", command=self.clear_text)
        self.button_clear.pack()

        # On-screen keyboard
        self.keyboard = tk.Frame(self)
        self.keyboard.pack()

        for row_idx, row in enumerate(key_layout):
            for col_idx, key in enumerate(row):
                button = self.create_keyboard_button(key)
                button.grid(row=row_idx, column=col_idx, padx=2, pady=2)

        #self.made_by_label = tk.Label(self, text="Made by ElliNet13")
        #self.made_by_label.pack()

    def clear_text(self):
        self.tf.delete(0, tk.END)

    def create_keyboard_button(self, text):
        if text == "ENTER":
            button = tk.Button(self.keyboard, text=text, command=self.return_value)
        else:
            button = tk.Button(self.keyboard, text=text, command=lambda t=text: self.handle_button_click(t))
        button.config(width=5, height=2)
        return button

    def handle_button_click(self, text):
        if text == "SPACE":
            self.tf.insert(tk.END, " ")
        elif text == "BACKSPACE":
            current_text = self.tf.get()
            if current_text:
                self.tf.delete(len(current_text) - 1, tk.END)
        else:
            self.tf.insert(tk.END, text)

    def return_value(self):
        self.value = self.tf.get()
        self.destroy()

class OnScreenKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.value = None

        self.title("On-Screen Keyboard")
        self.geometry("700x300")

        self.tf = tk.Entry(self)
        self.tf.pack()
        self.tf.config(width=40)

        self.label = tk.Label(self, text="")
        self.label.pack()

        self.button_clear = tk.Button(self, text="Clear", command=self.clear_text)
        self.button_clear.pack()

        # On-screen keyboard
        self.keyboard = tk.Frame(self)
        self.keyboard.pack()

        key_layout = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"],
            ["SPACE", "BACKSPACE"],
            ["ENTER"]
        ]

        for row_idx, row in enumerate(key_layout):
            for col_idx, key in enumerate(row):
                button = self.create_keyboard_button(key)
                button.grid(row=row_idx, column=col_idx, padx=2, pady=2)

        #self.made_by_label = tk.Label(self, text="Made by ElliNet13")
        #self.made_by_label.pack()

    def clear_text(self):
        self.tf.delete(0, tk.END)

    def create_keyboard_button(self, text):
        if text == "ENTER":
            button = tk.Button(self.keyboard, text=text, command=self.return_value)
        else:
            button = tk.Button(self.keyboard, text=text, command=lambda t=text: self.handle_button_click(t))
        button.config(width=5, height=2)
        return button

    def handle_button_click(self, text):
        if text == "SPACE":
            self.tf.insert(tk.END, " ")
        elif text == "BACKSPACE":
            current_text = self.tf.get()
            if current_text:
                self.tf.delete(len(current_text) - 1, tk.END)
        else:
            self.tf.insert(tk.END, text)

    def return_value(self):
        self.value = self.tf.get()
        self.destroy()

def gettinput():
    app = OnScreenKeyboard()
    app.mainloop()
    return app.value

def getcinput(name, key_layout, size):
    app = OnScreenCustom(name, key_layout, size)
    app.mainloop()
    return app.value

def getninput():
    app = OnScreenNumpad()
    app.mainloop()
    try:
      return 0 if app.value is None else app.value
    except ValueError:
      return 0