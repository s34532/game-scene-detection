import tkinter as tk
from tkinter import ttk
import threading
import os
import signal

# Your import statements for other modules here

# Function to run your main script in a separate thread
def run_script():
    global script_thread
    script_thread = threading.Thread(target=main_script)
    script_thread.start()

# Function to stop the running script
def stop_script():
    global script_thread
    if script_thread and script_thread.is_alive():
        os.kill(script_thread.ident, signal.CTRL_C_EVENT)

# Your main script function
def main_script():
    # Your existing code here

# Create the main window
root = tk.Tk()
root.title("Script GUI")

# Create and configure the GUI elements
frame = ttk.Frame(root)
frame.grid(column=0, row=0, padx=10, pady=10)

play_button = ttk.Button(frame, text="Play", command=run_script)
stop_button = ttk.Button(frame, text="Stop", command=stop_script)

play_button.grid(column=0, row=0, padx=5)
stop_button.grid(column=1, row=0, padx=5)

# Start the GUI main loop
root.mainloop()
