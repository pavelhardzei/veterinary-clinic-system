import tkinter as tk
from tkinter import ttk
import psycopg2


class CRUDForm:

    def __init__(self, root: tk.Tk, connection: psycopg2._psycopg.connection, cursor: psycopg2._psycopg.cursor):
        self.__connection = connection
        self.__cursor = cursor

        self.__crud_form = tk.Toplevel(root)
        self.__crud_form.title("CRUD Form")
        self.__width = 600
        self.__height = 400
        self.__crud_form.wm_minsize(self.__width, self.__height)
        self.__crud_form.geometry("+{}+{}".
                                  format(int(self.__crud_form.winfo_screenwidth() / 2 - self.__width / 2),
                                         int(self.__crud_form.winfo_screenheight() / 2 - self.__height / 2)))
        self.__crud_form.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

        self.__root_frame = tk.Frame(master=self.__crud_form)

        self.__headline_frame = tk.Frame(master=self.__root_frame)

        __lbl = tk.Label(master=self.__headline_frame, text="Tables", font="Times 16")
        __lbl.grid(row=0, column=0, columnspan=4, pady=15)

        __appointments = tk.Button(master=self.__headline_frame, text="Appointments", background="#555",
                                   foreground="#ccc", padx="10", pady="5", font="Times 14",
                                   command=self.__open_appointments)
        __appointments.grid(row=1, column=0, padx=10)
        __clients = tk.Button(master=self.__headline_frame, text="Clients", background="#555", foreground="#ccc",
                              padx="10", pady="5", font="Times 14",
                              command=self.__open_clients)
        __clients.grid(row=1, column=1, padx=10)
        __patients = tk.Button(master=self.__headline_frame, text="Patients", background="#555", foreground="#ccc",
                               padx="10", pady="5", font="Times 14",
                               command=self.__open_patients)
        __patients.grid(row=1, column=2, padx=10)
        __doctors = tk.Button(master=self.__headline_frame, text="Doctors", background="#555", foreground="#ccc",
                              padx="10", pady="5", font="Times 14",
                              command=self.__open_doctors)
        __doctors.grid(row=1, column=3, padx=10)

        self.__headline_frame.grid(row=0, column=0)

        self.__table_frame = tk.Frame(master=self.__root_frame)

        self.__table = ttk.Treeview(master=self.__table_frame)
        self.__table.column("#0", width=int(self.__width * 0.9))
        self.__table.grid(row=0, column=0)

        self.__scrollbar = ttk.Scrollbar(master=self.__table_frame, orient=tk.VERTICAL, command=self.__table.yview)
        self.__table.config(yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.grid(row=0, column=1, sticky="ns")

        self.__table_frame.grid(row=1, column=0, pady=30)

        self.__root_frame.pack()

    def __open_appointments(self):
        self.__create_table(("id", "client_id", "pet_id", "date", "time"))
        self.__cursor.execute("SELECT * FROM appointments;")
        self.__fill_table(self.__cursor.fetchall())

    def __open_clients(self):
        self.__create_table(("id", "name", "telephone", "pet_id"))
        self.__cursor.execute("SELECT * FROM clients;")
        self.__fill_table(self.__cursor.fetchall())

    def __open_patients(self):
        self.__create_table(("id", "name", "age", "owner_id", "kind"))
        self.__cursor.execute("SELECT * FROM patients;")
        self.__fill_table(self.__cursor.fetchall())

    def __open_doctors(self):
        self.__create_table(("id", "name", "salary"))
        self.__cursor.execute("SELECT * FROM doctors;")
        self.__fill_table(self.__cursor.fetchall())

    def __create_table(self, columns):
        self.__table.destroy()
        self.__table = ttk.Treeview(master=self.__table_frame)
        self.__table['columns'] = columns
        self.__table.column("#0", width=0, stretch=tk.NO)
        self.__table.heading("#0", text='')
        for column in columns:
            self.__table.column(column, anchor=tk.CENTER, width=int(0.9 * self.__width / len(columns)))
            self.__table.heading(column, text=column, anchor=tk.CENTER)

        self.__table.grid(row=0, column=0)
        self.__scrollbar.config(command=self.__table.yview)
        self.__table.config(yscrollcommand=self.__scrollbar.set)

    def __fill_table(self, records: list[tuple]):
        index = 0
        for record in records:
            self.__table.insert(parent='', index='end', iid=index, text='', values=record)
            index += 1