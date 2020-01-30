'''
taken from >> https://stackoverflow.com/questions/16745507/tkinter-how-to-use-threads-to-preventing-main-event-loop-from-freezing
modified by lalamax3d@gmail.com
'''
import queue
import tkinter
import threading
from tkinter import ttk
import time
class GUI:
    def __init__(self, master):
        self.master = master
        self.test_button = tkinter.Button(self.master, command=self.tb_click)
        self.test_button.configure( text="Start", background="Grey", padx=50)
        self.test_button.pack(side=tkinter.TOP)

    def progress(self):
        self.prog_bar = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="indeterminate" )
        self.prog_bar.pack(side=tkinter.TOP)

    # def tb_click(self):
    #     self.progress()
    #     self.prog_bar.start()
    #     # Simulate long running process
    #     t = threading.Thread(target=time.sleep, args=(5,))
    #     t.start()
    #     t.join()
    #     self.prog_bar.stop()
    def tb_click(self):
        self.progress()
        self.prog_bar.start()
        self.queue = queue.Queue()
        ThreadedTask(self.queue).start()
        self.master.after(100, self.process_queue)

    def process_queue(self):
        print ("Processing Queue From main..")
        try:
            msg = self.queue.get(0)
            # Show result of the task if needed
            if msg == 'Task finished':
                # self.prog_bar['value'] = 100
                self.prog_bar.stop()
            else:
                print ("progressing..",msg)
            self.master.after(1000, self.process_queue)
        except queue.Empty:
            self.master.after(100, self.process_queue)

class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        print ("Thread starting (long task)")
        for i in range (5):
            self.queue.put("Task Progressing")
            time.sleep(1)  # Simulate long running process
        self.queue.put("Task finished")

root = tkinter.Tk(  )
root.title("Test Button")
main_ui = GUI(root)
root.mainloop()
