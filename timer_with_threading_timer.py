from threading import Timer
from threading import Thread
import time
from time import sleep
import datetime
import tkinter as tk  # GUI
from tkinter import ttk  # GUI
from tkinter import messagebox # GUI

class AppGui(tk.Tk):
    def __init__(self):
        """ GUI Setting Starts Here """
        super().__init__()  # Inheritance from tkinter class
        self.title("Timer Sample")
        self.geometry("600x100")
        self.resizable(0, 0)

        self.reactor_timer = None

        self.time_left_label = tk.Label(self, text="Time Left:")
        self.time_left_label.grid(column=0, row=1)

        self.time_left = tk.Label(self, text=5)
        self.time_left.grid(column=1, row=1)

        self.count_rotation_label = tk.Label(self, text="Count Every(min):")
        self.count_rotation_label.grid(column=0, row=2)

        self.start_button = tk.Button(self, overrelief="solid", width=15, text="Start", repeatdelay=1000, repeatinterval=100,
                                 command=lambda: self.start_button_clicked())
        self.start_button.grid(column=0, row=3)
        """ GUI Setting Ends Here """

    def start_button_clicked(self):
        # If Tick Starts, start a new thread
        if self.start_button['text'] == 'Start':
            # Set Timer
            self.reactor_timer = Repeated_Timer(1, self.timer_tick_event)
            self.reactor_timer.start()

            self.start_button['text'] = 'Stop'
            self.start_button.configure(fg='red')

        # If Tick Stopped, initialize everything
        # + Once variables are initialized, pre-exist thread will be stopped automatically
        else:
            self.reactor_timer.stop()

            self.time_left['text'] = '0'
            self.start_button['text'] = 'Start'
            self.start_button.configure(fg='black')

            #self.reactor_timer = None

    def timer_tick_event(self):
        print('hello')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.reactor_timer != None:
                self.reactor_timer.stop()
            self.destroy()


class Repeated_Timer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

#interval = 5
#reactor_timer = Repeated_Timer(interval, timer_tick_event)
#reactor_timer.start()

# reactor_timer.stop()


if __name__ == '__main__':
    app = AppGui()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()  # execute GUI
