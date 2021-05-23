import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from crud_form import CRUDForm


class AuthorizationForm:

    def __init__(self):
        self.__connection = psycopg2.connect(user="pavelhardzei", password="1234", host="127.0.0.1",
                                             port="5432", database="vet_clinic")
        self.__cursor = self.__connection.cursor()

        self.__root = tk.Tk()
        self.__root.title("Veterinary Clinic")
        self.__width = 400
        self.__height = 300
        self.__root.wm_minsize(self.__width, self.__height)
        self.__root.geometry("+{}+{}".
                             format(int(self.__root.winfo_screenwidth() / 2 - self.__width / 2),
                                    int(self.__root.winfo_screenheight() / 2 - self.__height / 2)))
        self.__root.resizable(False, False)
        __frame = tk.Frame(master=self.__root)

        __lbl = tk.Label(master=__frame, text="Authorization", font="Times 16")
        __lbl.grid(row=0, column=0, columnspan=2, pady="5")

        __login_label = tk.Label(master=__frame, text="Login", font="Times 16")
        __login_label.grid(row=1, column=0, pady="5", padx="10")
        self.__login_message = tk.StringVar()
        __login_entry = tk.Entry(master=__frame, textvariable=self.__login_message, font="Times 16")
        __login_entry.grid(row=1, column=1, pady="5")

        __password_label = tk.Label(master=__frame, text="Password", font="Times 16")
        __password_label.grid(row=2, column=0, pady="5", padx="10")
        self.__password_message = tk.StringVar()
        __password_entry = tk.Entry(master=__frame, textvariable=self.__password_message, font="Times 16", show="*")
        __password_entry.grid(row=2, column=1, pady="5")

        __sign_in = tk.Button(master=__frame, text="Sign in", background="#555", foreground="#ccc",
                              padx="10", pady="5", font="Times 14", command=self.__sign_in_handler)
        __sign_in.grid(row=3, column=0, padx="20", pady="20", columnspan=2)

        __frame.place(relx=0.5, rely=0.5, anchor="c")

        self.__root.mainloop()

    def __sign_in_handler(self):
        try:
            if self.__login_message.get().replace(" ", "") == "" or \
                    self.__password_message.get().replace(" ", "") == "":
                raise Exception("Empty fields")

            self.__cursor.execute("SELECT password FROM users WHERE login=%s;", [self.__login_message.get().strip()])

            records = self.__cursor.fetchall()
            if len(records) < 0:
                raise Exception("Login or password are incorrect")

            correct = False
            for password in records:
                if password[0] == self.__password_message.get().strip():
                    correct = True
                    break

            if not correct:
                raise Exception("Login or password are incorrect")

            CRUDForm(self.__root, None, None)
            self.__root.withdraw()
        except Exception as e:
            messagebox.showinfo("Exception", e)

    def __del__(self):
        self.__connection.close()
        self.__cursor.close()