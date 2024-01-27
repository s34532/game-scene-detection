from tkinter import Toplevel, messagebox, ttk
from PIL import Image, ImageTk
import tkinter as tk
import mss.tools
import mss


sct = mss.mss()
combSelect = ""

    
def create_list(r2):
    return list(map(lambda x: x, range(1, r2+1)))


def display_selection(combo):
    global combSelect
    combSelect = combo.get()
    selection = int(combSelect)
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[selection])

        # Convert to PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
    

        # Create a new window
        top = Toplevel()
        top.title(f"Monitor {selection}")

        # Convert to ImageTk format and display
        new_width = 800
        ratio = new_width / img.width
        new_height = int(img.height * ratio)

        resized = img.resize((new_width, new_height), Image.ANTIALIAS)
        tk_img = ImageTk.PhotoImage(resized)
        label = tk.Label(top, image=tk_img)
        label.image = tk_img  # Keep a reference!
        label.pack()

def start_program():
    global combSelect
    if combSelect == "":
        messagebox.showinfo(
        message=f"Please select a monitor by clicking the dropdown box then clicking 'Select Monitor'!",
        title="Selection"
    )
    else:
        main()

    


def main():
    monitors_list = []  
    choices = []

    for monitor in sct.monitors[1:]:  
            monitors_list.append(monitor)

    print(len(sct.monitors[1:]))

    choices = create_list(len(sct.monitors[1:]))

    print(choices)

        

    main_window = tk.Tk()

    window_width = 700
    window_height = 700
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    main_window.config(width=window_width, height=window_height)
    main_window.title("Wizard101 Vestrilund settings")
        
    combo = ttk.Combobox(
        state="readonly",
        values=choices
    )
    combo.place(x=50, y=50)
    button1 = ttk.Button(text="Select Monitor", command=lambda: display_selection(combo))
    button1.place(x=50, y=100)

    button2 = ttk.Button(text="Start Program", command = lambda: start_program())
    button2.place(x=50, y=150)


    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    main_window.geometry(f'+{x}+{y}')
    main_window.mainloop()

if __name__ == "__main__":
    main()

