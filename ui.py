from tkinter import Button, Entry, Tk, PhotoImage, Frame, Label, messagebox, NO
from utils import config_get, get_captcha, md5
from database import DatabaseManager
from tkinter import ttk
import tkinter as tk
import tkinter.ttk as ttk
from string import ascii_uppercase, ascii_lowercase


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert("", tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


class Window:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry("300x370+0+0")
        # self.root.resizable(True, True)
        self.root.eval("tk::PlaceWindow . center")
        self.root.title("Чеботарёв Степан ПКС-405")
        self.root.iconphoto(False, PhotoImage(file=config_get("icon_path")))
        self.Frame = None
        self.database_manager = DatabaseManager()

        # ? Fonts
        self.font_color = "#37474F"
        self.font_color_complementary = "#78909C"
        self.font_color_accent = "#FF9C1A"
        self.font_captcha = ("Curlz MT", 24)
        self.font_20 = (
            "Arial",
            20,
        )
        self.font_24 = (
            "Arial",
            24,
        )
        self.font_28 = (
            "Arial",
            28,
        )

    def MainPage(self):
        self.root.geometry("1600x600+0+0")
        self.root.title("My Best Program")
        self.root.eval("tk::PlaceWindow . center")
        self.Frame = Frame(self.root, bg="white")
        self.Frame.place(x=0, y=0)

        self.Treeview = Table(
            self.Frame,
            headings=(
                "Артикул",
                "Наименование",
                "Единица изменения",
                "Количество",
                "Поставщик",
                "Тип",
                "Цена",
                "Вес",
            ),
            rows=(self.database_manager.get_all_fittings()),
        )
        self.Treeview.pack(expand=tk.YES, fill=tk.BOTH)

    def LoginPage(self) -> None:
        if type(self.Frame) is Frame:
            self.Frame.destroy()

        self.Frame = Frame(self.root, width=300, height=400)
        self.Frame.grid(row=0, column=0, sticky="NW")
        self.Frame.grid_propagate(0)
        self.Frame.update()
        self.root.title("Авторизация")

        label = Label(
            self.Frame, text="Login here", font=self.font_24, fg=self.font_color
        )

        label.place(
            x=self.Frame.winfo_width() / 2,
            y=self.Frame.winfo_height() / 2 - 150,
            anchor="center",
        )

        username_label = Label(
            self.Frame, text="Username", font=self.font_24, fg=self.font_color
        )

        username_label.place(
            x=self.Frame.winfo_width() / 2 - 70,
            y=self.Frame.winfo_height() / 2 - 100,
            anchor="center",
        )

        password_label = Label(
            self.Frame, text="Password", font=self.font_24, fg=self.font_color
        )

        password_label.place(
            x=self.Frame.winfo_width() / 2 - 70,
            y=self.Frame.winfo_height() / 2 - 30,
            anchor="center",
        )

        self.captcha_answer = get_captcha()

        self.captcha_label = Label(
            self.Frame,
            text=self.captcha_answer,
            font=self.font_captcha,
            fg=self.font_color_complementary,
        )

        self.captcha_label.place(
            x=self.Frame.winfo_width() / 2 - 80,
            y=self.Frame.winfo_height() / 2 + 40,
            anchor="center",
        )

        self.username = Entry(
            self.Frame, font=self.font_20, fg=self.font_color, width=20
        )
        self.password = Entry(
            self.Frame, font=self.font_20, fg=self.font_color, show="*", width=20
        )

        self.username.place(
            x=self.Frame.winfo_width() / 2,
            y=self.Frame.winfo_height() / 2 - 70,
            anchor="center",
        )
        self.password.place(
            x=self.Frame.winfo_width() / 2,
            y=self.Frame.winfo_height() / 2,
            anchor="center",
        )

        self.captcha = Entry(
            self.Frame, font=self.font_20, fg=self.font_color, width=20
        )

        self.captcha.place(
            x=self.Frame.winfo_width() / 2,
            y=self.Frame.winfo_height() / 2 + 70,
            anchor="center",
        )

        sign_in_button = Button(
            self.Frame,
            text="Sign In",
            font=self.font_20,
            width=9,
            fg="green",
            command=self.sign_in,
        )
        sign_up_button = Button(
            self.Frame,
            text="Sign Up",
            font=self.font_20,
            width=9,
            fg="blue",
            command=self.sign_up,
        )

        sign_in_button.place(
            x=self.Frame.winfo_width() / 2 - 70,
            y=self.Frame.winfo_height() / 2 + 120,
            anchor="center",
        )

        sign_up_button.place(
            x=self.Frame.winfo_width() / 2 + 69,
            y=self.Frame.winfo_height() / 2 + 120,
            anchor="center",
        )
        return

    def update_captcha(self) -> None:
        self.captcha_answer = get_captcha()
        self.captcha_label.destroy()
        self.captcha_label = Label(
            self.Frame,
            text=self.captcha_answer,
            font=self.font_captcha,
            fg=self.font_color_complementary,
        )

        self.captcha_label.place(
            x=self.Frame.winfo_width() / 2 - 80,
            y=self.Frame.winfo_height() / 2 + 40,
            anchor="center",
        )

    def sign_in(self) -> None:
        captcha = self.captcha.get()

        if not captcha or captcha.strip() != self.captcha_answer:
            self.update_captcha()
            messagebox.showerror("Регистрация", "Ошибка в капче!", icon="warning")
            return

        login, password = self.username.get(), self.password.get()

        is_sign_in = self.database_manager.sign_in(login, md5(password))

        if is_sign_in:
            # * Очистка фрейма, мусорных атрибутов
            self.Frame.destroy()
            del self.Frame
            del self.username
            del self.password
            del self.captcha

            # * Инициализация основной страницы
            self.MainPage()

            return True
        self.update_captcha()
        messagebox.showerror(
            "Авторизация", "Логин и/или пароль неверны!", icon="warning"
        )

        return False

    def sign_up(self) -> None:
        from re import compile

        captcha = self.captcha.get()

        if not captcha or captcha.strip() != self.captcha_answer:
            self.update_captcha()

            messagebox.showerror("Регистрация", "Ошибка в капче!", icon="warning")
            return

        login, password = self.username.get(), self.password.get()

        password_len = len(password)

        if password_len < 6:
            messagebox.showerror(
                "Регистрация",
                "В пароле должно быть не менее 6 символов!",
                icon="warning",
            )
            return

        elif password_len > 18:
            messagebox.showerror(
                "Регистрация",
                "В пароле должно быть не более 18 символов!",
                icon="warning",
            )
            return

        symbol_in = False
        number_in = False
        low_in = False
        up_in = False
        stack = []
        not3_in = True

        numbers = list(map(str, (range(10))))

        for symbol in password:
            if symbol in ["*", "&", "{", "}", "|", ".", "+"]:
                symbol_in = True

            if symbol in numbers:
                number_in = True

            if symbol in ascii_lowercase:
                low_in = True

            if symbol in ascii_uppercase:
                low_in = True

            if not3_in:

                if not stack:
                    stack = [symbol]

                elif symbol == stack[0]:
                    if len(stack) == 2:
                        not3_in = False

                    symbol.append(symbol)
                else:
                    stack = [symbol]

        if not low_in:
            self.update_captcha()

            messagebox.showerror(
                "Регистрация",
                "Вы забыли указать буквы нижнего регистра!",
                icon="warning",
            )
            return

        if not up_in:
            self.update_captcha()

            messagebox.showerror(
                "Регистрация", "Вы забыли указать заглавные буквы!", icon="warning"
            )
            return

        if not symbol_in:
            self.update_captcha()

            messagebox.showerror(
                "Регистрация", "Вы забыли указать символ!", icon="warning"
            )
            return

        if not number_in:
            self.update_captcha()

            messagebox.showerror(
                "Регистрация", "Вы забыли указать число!", icon="warning"
            )
            return

        result = self.database_manager.sign_up(login, md5(password))

        if not result:
            self.update_captcha()
            messagebox.showerror("Регистрация", "Ошибка регистрации!", icon="warning")
            return

        messagebox.showinfo("Регистрация", "Пользователь успешно зарегистрирован!")

    def Run(self) -> None:
        self.LoginPage()

        return self.root.mainloop()
