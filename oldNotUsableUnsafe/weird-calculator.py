import tkinter as tk
import webbrowser
import random

root = tk.Tk()
root.title("Pico Calculator")

entry = tk.Entry(root, width=25, font=("Segoe UI", 14))
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

# track presses
press_count = 0
# list of easter egg urls
urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # never gonna give you up
    "https://c418.bandcamp.com/track/beginning-2",   # beginning 2
    "https://www.raspberrypi.com/"                   # raspberry pi
]

# function to handle button clicks
def click(symbol):
    entry.insert(tk.END, symbol)

def clear():
    entry.delete(0, tk.END)

def evaluate():
    global press_count
    expr = entry.get().strip().lower()

    # normal easter eggs by code
    if expr == "picoegg1":
        webbrowser.open(urls[0])
        return
    elif expr == "picoegg2":
        webbrowser.open(urls[1])
        return
    elif expr == "picoegg3":
        webbrowser.open(urls[2])
        return

    # increment press count and maybe open random url
    press_count += 1
    if press_count % 2 == 0:  # every 2 presses
        webbrowser.open(random.choice(urls))

    # do normal calculation
    try:
        result = eval(expr)
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "error")

# layout
buttons = [
    '7','8','9','/',
    '4','5','6','*',
    '1','2','3','-',
    '0','.','=','+'
]

row = 1
col = 0
for b in buttons:
    if b == "=":
        tk.Button(root, text=b, width=5, height=2, command=evaluate).grid(row=row, column=col)
    else:
        tk.Button(root, text=b, width=5, height=2, command=lambda x=b: click(x)).grid(row=row, column=col)
    col += 1
    if col > 3:
        col = 0
        row += 1

tk.Button(root, text="C", width=5, height=2, command=clear).grid(row=row, column=0)

root.mainloop()
