import tkinter as tk
import math

rows = [
    "1234567890-=",
    "qwertyuiop[]",
    "asdfghjkl;'\"",
    "zxcvbnm,./\\⌫"
]

arrows = ["Up", "Right", "Down", "Left"]
arrow_symbols = {"Up": "↑", "Right": "→", "Down": "↓", "Left": "←"}
arrow_to_index = {k: i for i, k in enumerate(arrows)}

BACKSPACE_GESTURE = ["Left", "Left", "Down"]


def split4(seq):
    n = len(seq)
    size = math.ceil(n / 4)
    return [seq[i*size:(i+1)*size] for i in range(4)]


def resolve(buffer):
    """Decode buffer to possible candidates, layer2, layer3"""
    buffer = [b for b in buffer if b in arrow_to_index]

    if not buffer:
        return [], {}, {}

    row_index = arrow_to_index[buffer[0]] if buffer[0] in arrow_to_index else 0
    row_chars = rows[row_index]

    group = row_chars
    for a in buffer[1:]:
        if len(group) <= 1:
            break
        group = split4(group)[arrow_to_index[a]]

    candidates = list(group)
    layer2 = {}
    layer3 = {}

    if len(group) > 1:
        l2 = split4(group)
        for i, part in enumerate(l2):
            for ch in part:
                layer2[ch] = arrows[i]
        for i, part in enumerate(l2):
            if len(part) <= 1:
                continue
            l3 = split4(part)
            for j, sub in enumerate(l3):
                for ch in sub:
                    layer3[ch] = (arrows[i], arrows[j])

    return candidates, layer2, layer3


class Keyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Arrow Virtual Keyboard")

        self.buffer = []
        self.locked = False

        self.display = tk.Entry(root, font=("Arial", 16), width=40)
        self.display.grid(row=0, column=0, columnspan=20)

        self.output = tk.Entry(root, font=("Arial", 16), width=40)
        self.output.grid(row=1, column=0, columnspan=20)

        self.keys = {}
        self.row_badges = {}

        self.build_keyboard()
        self.render()

        root.bind("<Up>", self.on_key)
        root.bind("<Right>", self.on_key)
        root.bind("<Down>", self.on_key)
        root.bind("<Left>", self.on_key)
        root.bind("<BackSpace>", self.on_key)

    def build_keyboard(self):
        for r, row in enumerate(rows):
            for c, k in enumerate(row):
                self.make_virtual_key(k, r + 2, c)

            badge = tk.Label(self.root, text="", font=("Arial", 16, "bold"),
                             fg="red", bg="white")
            badge.grid(row=r + 2, column=len(row), padx=2, pady=2)
            self.row_badges[r] = badge

    def make_virtual_key(self, char, row, col):
        btn = tk.Button(
            self.root,
            text=char,
            width=5,
            height=2,
            font=("Arial", 11),
            command=lambda c=char: self.virtual_key_pressed(c)
        )
        btn.grid(row=row, column=col, padx=2, pady=2)
        self.keys[char] = btn

    def virtual_key_pressed(self, char):
        if char == "⌫":
            self.apply_backspace()
            return

        if char in arrow_to_index:
            self.process_arrow(char)

    def process_arrow(self, key):
        self.buffer.append(key)
        self.display.insert(tk.END, arrow_symbols[key])

        if len(self.buffer) >= 3 and self.buffer[-3:] == BACKSPACE_GESTURE:
            # remove gesture
            self.buffer = self.buffer[:-3]
            self.apply_backspace()
            self.reset()
            return

        self.render()
        c, _, _ = resolve(self.buffer)
        if len(c) == 1:
            self.output.insert(tk.END, c[0])
            self.flash(c[0])

    def apply_backspace(self):
        if len(self.buffer) > 0:
            self.buffer.pop()
            self.display.delete(0, tk.END)
            self.display.insert(0, "".join(arrow_symbols[b] for b in self.buffer))
            self.render()
            return

        txt = self.output.get()
        if len(txt) > 0:
            self.output.delete(len(txt) - 1, tk.END)

    def on_key(self, e):
        if self.locked:
            return

        if e.keysym == "BackSpace" or e.char == "⌫":
            self.apply_backspace()
            return

        if e.keysym in arrow_to_index:
            self.process_arrow(e.keysym)

    def render(self):
        candidates, layer2, layer3 = resolve(self.buffer)

        for r in range(len(rows)):
            self.row_badges[r].config(text=arrow_symbols[arrows[r]])

        for k in self.keys:
            self.keys[k].config(bg="white", text=k)

        for ch, d in layer2.items():
            if ch in self.keys:
                self.keys[ch].config(text=f"{ch} {arrow_symbols[d]}")

        for ch, (d1, d2) in layer3.items():
            if ch in self.keys:
                self.keys[ch].config(text=f"{ch} {arrow_symbols[d1]}{arrow_symbols[d2]}")

        if len(candidates) == 1 and candidates[0] in self.keys:
            self.keys[candidates[0]].config(bg="lightgreen")

    def flash(self, ch):
        self.locked = True
        self.keys[ch].config(bg="lightgreen")
        self.root.after(250, self.reset)

    def reset(self):
        self.buffer.clear()
        self.display.delete(0, tk.END)
        self.locked = False
        self.render()

    def run(self):
        self.root.mainloop()


root = tk.Tk()
Keyboard(root).run()
