# Libraries
import tkinter as tk  # GUI
from tkinter import ttk  # GUI
from tkinter import messagebox  # GUI
import threading # Thread
import time

DEFAULT_MIN_LEFT = 3                        # How long left in min as default
DEFAULT_SEC_LEFT = 60                       # How Long left in sec as default

sec_per_tick = 1                            # determines how fast the tick will be
time_left_in_min = DEFAULT_MIN_LEFT         # time left in min
time_left_in_sec = DEFAULT_SEC_LEFT         # time left in sec
thread_id = 0                               # shows which thread is active

class App(tk.Tk):
    def __init__(self):
        global time_left_in_min, time_left_in_sec

        # ticks every n min
        rotation_period_min = [1, 5, 10, 15]

        """ GUI Setting Starts Here """
        super().__init__()  # Inheritance from tkinter class
        self.title("Timer Sample")
        self.geometry("600x100")
        self.resizable(0, 0)

        time_left_label = tk.Label(self, text="Time Left:")
        time_left_label.grid(column=0, row=1)

        time_left = tk.Label(self, text=time_left_in_min)
        time_left.grid(column=1, row=1)

        count_rotation_label = tk.Label(self, text="Count Every(min):")
        count_rotation_label.grid(column=0, row=2)

        count_rotation_combo = ttk.Combobox(self, state="readonly", width=50, values=rotation_period_min)
        count_rotation_combo.grid(column=1, row=2)
        count_rotation_combo.current(0)

        start_button = tk.Button(self, overrelief="solid", width=15, text="Start", repeatdelay=1000, repeatinterval=100,
                                 command=lambda: Function.start_button_clicked(start_button, count_rotation_combo, time_left))
        start_button.grid(column=0, row=3)
        """ GUI Setting Ends Here """


class Function:
    @staticmethod
    def start_button_clicked(start_button, count_rotation_combo, time_left):
        global sec_per_tick, thread_id

        # If Tick Starts, start a new thread
        if start_button['text'] == 'Start':
            sec_per_tick = int(count_rotation_combo.get())*60 # multiplies by 60 for it is based on minute(not second)
            thread = threading.Thread(target=Function.start_tick, args=(time_left,start_button, thread_id,), daemon=True)
            thread.start()

            start_button['text'] = 'Stop'
            start_button.configure(fg='red')

        # If Tick Stopped, initialize everything
        # + Once variables are initialized, pre-exist thread will be stopped automatically
        else:
            Function.initialize_vars(time_left, start_button)

    def initialize_vars(time_left, start_button):
        global time_left_in_min, time_left_in_sec, thread_id

        thread_id += 1
        time_left_in_min = DEFAULT_MIN_LEFT   # initialize
        time_left_in_sec = DEFAULT_SEC_LEFT
        time_left['text'] = time_left_in_min
        start_button['text'] = 'Start'
        start_button.configure(fg='black')

    def start_tick(time_left, start_button, id):
        global sec_per_tick, time_left_in_min, time_left_in_sec, thread_id

        print("Tick Started")
        while thread_id == id: # This thread will be stopped automatically, once thread_id is changed
            print(time.ctime(), "\t\ttick time: ", sec_per_tick)

            if time_left_in_min == 1: # if left time is less than 1 min, count every 1 sec
                time_left['text'] = time_left_in_sec # change text
                sec_per_tick = 1
                time_left_in_sec -= 1
            else: # if left time is greater than 1 min, count every min after following how "count_rotation_combo" indicates
                time_left['text'] = time_left_in_min # change text
                time_left_in_min -= 1

            time.sleep(sec_per_tick)

            if time_left_in_sec < 0: # once all count is done, pop up window
                messagebox.showinfo("Tick Done")
                Function.initialize_vars(time_left, start_button)
                break # finish thread

if __name__ == '__main__':
    app = App()
    app.mainloop()  # execute GUI
