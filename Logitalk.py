from customtkinter import *
import socket
import threading

class MyWin(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('400x300')
        self.title('Stas')
        self.scale = 1.5
        self.username = "User"

        self.frame = CTkFrame(self, width=0, fg_color='light blue')
        self.frame.pack_propagate(False)
        self.frame.place(x=0, y=0)

        self.btn = CTkButton(self, text='▶️', command=self.click, width=30)
        self.btn.place(x=0, y=0)

        self.is_show_menu = False
        self.frame_width = 0

        self.emp = CTkEntry(self.frame, width=0, placeholder_text="Введіть ім'я")
        self.emp.pack(pady=20)
        self.emp_height = 0
        self.emp_width = 0

        self.but_name = CTkButton(self.frame, width=0, text=">", command=self.change_name)
        self.but_name.place(x=self.emp.winfo_height() + 20, y=40)

        self.entry = CTkEntry(self, placeholder_text='Введіть повідомлення:')
        self.btn_send = CTkButton(self, text='>', width=28, command=self.send_message)

        self.menu = CTkOptionMenu(self.frame, values=["Світла", "Темна"], command=self.change_theme)
        self.menu.set("Світла")
        self.menu.pack(pady=20)

        self.text_box = CTkTextbox(self, height=220)
        self.text_box.configure(state="disabled")

        self.update_ui()

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('127.0.0.1', 8080))
            hello = f"{self.username} приєднався до чату"
            self.socket.send(hello.encode())
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.display_message(f"Не вдалось підключитись до сервера: {e}")

    def recv_message(self):
        while True:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                message = data.decode("utf-8")
                self.after(0, self.display_message, message)
            except:
                break

    def send_message(self):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, END)
        full_msg = f"{self.username}: {msg}"
        try:
            self.socket.send(full_msg.encode())
        except:
            self.display_message("❌ Помилка відправлення повідомлення.")
            return
        self.display_message(full_msg)

    def change_name(self):
        new_username = self.emp.get().strip()
        if new_username and new_username != self.username:
            msg = f"* {self.username} змінив ім'я на {new_username}"
            self.username = new_username
            try:
                self.socket.send(msg.encode())
            except:
                self.display_message("❌ Не вдалось надіслати зміну імені.")
            self.display_message(msg)

    def display_message(self, msg: str):
        self.text_box.configure(state="normal")
        self.text_box.insert("end", msg + "\n")
        self.text_box.configure(state="disabled")
        self.text_box.see("end")

    def click(self):
        if self.is_show_menu:
            self.btn.configure(text='◀️')
            self.is_show_menu = False
            self.hide_menu()
        else:
            self.btn.configure(text='▶️')
            self.is_show_menu = True
            self.show_menu()

    def update_ui(self):
        win_w = self.winfo_width() / self.scale
        win_h = self.winfo_height() / self.scale

        self.btn_send.place(x=win_w - 28, y=win_h - 28)
        self.entry.configure(width=win_w - 28 - self.frame.winfo_width() / self.scale)
        self.entry.place(x=self.frame.winfo_width() / self.scale, y=win_h - 28)
        self.text_box.configure(width=(win_w - 28 - self.frame.winfo_width()) - 20,
                                height=win_h - self.entry.winfo_height())
        self.text_box.place(x=self.frame.winfo_width() + 65 / self.scale, y=0)

        self.after(50, self.update_ui)

    def show_menu(self):
        if self.frame_width < 200:
            self.frame_width += 10
            self.emp_width += 8
            if self.emp_height < 40:
                self.emp_height += 1
            self.frame.configure(width=self.frame_width, height=self.winfo_height())
            self.emp.configure(width=self.emp_width, height=self.emp_height)
        if self.is_show_menu:
            self.after(10, self.show_menu)

    def hide_menu(self):
        if self.frame_width > 0:
            self.frame_width -= 10
            if self.emp_width > 0:
                self.emp_width -= 8
            if self.emp_height > 0:
                self.emp_height -= 1
            self.frame.configure(width=self.frame_width, height=self.winfo_height())
            self.emp.configure(width=self.emp_width, height=self.emp_height)
        if not self.is_show_menu:
            self.after(10, self.hide_menu)

    def change_theme(self, choice):
        if choice == "Темна":
            set_appearance_mode("dark")
            self.frame.configure(fg_color="dodger blue")
        else:
            set_appearance_mode("light")
            self.frame.configure(fg_color="light blue")


win = MyWin()
win.mainloop()
