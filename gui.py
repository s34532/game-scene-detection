from tkinter import *
from tkinter import ttk, messagebox
import ctypes
import tkinter
from mss import mss
import mss.tools
from PIL import Image, ImageTk


monitorMap = {
    "Monitor 1": 1,
    "Monitor 2": 2,
    "Monitor 3": 3,
    "Monitor 4": 4,
    "Monitor 5": 5,
    "Monitor 6": 6
}

def screen_cap(monitor_number):
    with mss.mss() as sct:
        # Get information of monitor 2
        output = "output\\output.png"
        # Grab the data
        sct_img = sct.grab(sct.monitors[monitor_number])

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print(output)


def createList(r2):
    string = "Monitor"
    temp = list(range(1,r2))
    new_list = [string + " " + str(x) for x in temp]
    return new_list


def start_exe(combo):
    if combo.get() == "":
        messagebox.showwarning("warning", "select a monitor")
    else:
        print(monitorMap[combo.get()])

def display_selection(combo):
    
    combSelect = combo.get()

    selection = monitorMap[combSelect]
    

    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[selection])

        # Convert to PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
    

        # Create a new window
        top = Toplevel()
        top.title(f"Monitor {selection}")

        # Convert to ImageTk format and display

        tk_img = ImageTk.PhotoImage(img)
        label = tkinter.Label(top, image=tk_img)
        label.image = tk_img  # Keep a reference!
        label.pack()



def main():
    sct = mss.mss()
    monitor = sct.monitors
    monitorList = createList(len(monitor))
    print(monitorList)

    
    




    root = Tk()

        # this will create a label widget
    l2 = Label(root, text = "Select monitor")
    l2.grid(row = 1, column = 1, sticky = W, pady = 10)

    # grid method to arrange labels in respective
    # rows and columns as specified

    root.title("Combobox")
    root.geometry('1280x720')
    combo = ttk.Combobox(root, values = monitorList)
    combo.grid(row = 2, column = 1, sticky = W, pady = 10)
    combo.bind("<<ComboboxSelected>>", lambda _ : display_selection(combo))

    startButton = Button(root, text = "Start bot", command = lambda: start_exe(combo))
    startButton.grid(row = 3, column = 1, sticky = W, pady = 10)

    stopButton = Button(root, text = "Stop bot", command = start_exe)
    stopButton.grid(row = 4, column = 1, sticky = W, pady = 10)


    mainloop()




if __name__ == "__main__":
    main()