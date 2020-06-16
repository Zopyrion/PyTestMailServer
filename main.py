import tkinter as tk
import pathlib
from config import MESSAGE_DIR, HOST
from mail_server_tool import run_server
import multiprocessing


class Application(tk.Frame):
    is_started = False
    server = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.set_options()

        self.port_input = None
        self.start = None

        self.create_widgets()
        self.pack()

    def set_options(self):
        self.master.title('Py Test Mail Server')
        self.master.minsize(width=600, height=250)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master['bg'] = 'black'

    def on_closing(self):
        if self.is_started:
            self.server.terminate()
        self.master.destroy()

    def create_widgets(self):

        port_label = tk.Label(self)
        port_label["text"] = "Port to listen on: "
        port_label.grid(sticky="W", row=0, column=1, padx=10, pady=25)

        self.port_input = tk.Spinbox(self, width=8, from_=0, to=65535, textvariable=tk.DoubleVar(value=25))
        self.port_input.grid(sticky="W", row=0, column=2, padx=10, pady=25)

        output_label = tk.Label(self)
        output_label["text"] = "Path of received emails: "
        output_label.grid(sticky="W", row=1, column=1, padx=10, pady=25)

        output_input = tk.Entry(self, width=70)
        output_input.insert(0, str(pathlib.Path(__file__).parent.absolute()) + "\\" + MESSAGE_DIR)
        output_input.grid(row=1, column=2, padx=10, pady=20)
        output_input.bind("<Key>", lambda e: "break")

        self.start = tk.Button(self, text="Start Server", width=12, height=2,
                               command=self.start_server, borderwidth=0, bg='#C6E8E8')
        self.start.grid(row=2, pady=50, columnspan=2, sticky='E')

        quit_button = tk.Button(self, text="QUIT", fg="red", width=12, height=2,
                                command=self.on_closing, borderwidth=0, bg='#C6E8E8')
        quit_button.grid(row=3, column=2, padx=50, pady=20, columnspan=2, sticky='E')

    def start_server(self):
        """
        Starts the email server and sets the GUI appropriately.
        """
        if self.is_started:
            self.server.terminate()
            self.start["text"] = "Start Server"
            self.port_input.config(state='normal')
        else:
            if not self.port_input.get().isdigit():
                return

            # Start email server on another thread
            self.server = multiprocessing.Process(target=run, args=(int(self.port_input.get()),))
            self.server.start()
            self.start["text"] = "Stop Server"
            self.port_input.config(state='disabled')

        self.is_started = not self.is_started


def run(port):
    """
    Runs the server on *port*.
    """
    run_server(HOST, port)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
