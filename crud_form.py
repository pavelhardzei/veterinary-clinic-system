import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox
import psycopg2


class CRUDForm:

    def __init__(self, root: tk.Tk, connection: psycopg2._psycopg.connection, cursor: psycopg2._psycopg.cursor):
        self.__connection = connection
        self.__cursor = cursor

        self.__textvariables: list[tk.StringVar] = []
        self.__current_table: str = ""

        self.__crud_form = tk.Toplevel(root)
        self.__crud_form.title("CRUD Form")
        self.__crud_form.resizable(False, False)
        self.__width = 650
        self.__height = 550
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

        self.__crud_frame = tk.Frame(master=self.__root_frame)

        self.__crud_frame.grid(row=2, column=0)

        self.__remove_frame = tk.Frame(master=self.__root_frame)
        tk.Button(master=self.__remove_frame, text="Remove All", background="#555", foreground="#ccc",
                  font="Times 11", command=self.__remove_all).grid(row=0, column=0, padx=int(self.__width * 0.15))
        tk.Button(master=self.__remove_frame, text="Remove Selected", background="#555", foreground="#ccc",
                  font="Times 11", command=self.__remove_selected).grid(row=0, column=1, padx=int(self.__width * 0.15))
        self.__remove_frame.grid(row=3, column=0, pady=30)

        self.__root_frame.pack()

    def __open_appointments(self):
        self.__create_table(("id", "client_id", "pet_id", "date", "time"))
        self.__current_table = "appointments"
        self.__cursor.execute("SELECT * FROM {};".format(self.__current_table))
        self.__fill_table(self.__cursor.fetchall())

    def __open_clients(self):
        self.__create_table(("id", "name", "telephone"))
        self.__current_table = "clients"
        self.__cursor.execute("SELECT * FROM {};".format(self.__current_table))
        self.__fill_table(self.__cursor.fetchall())

    def __open_patients(self):
        self.__create_table(("id", "name", "age", "owner_id", "kind"))
        self.__current_table = "patients"
        self.__cursor.execute("SELECT * FROM {};".format(self.__current_table))
        self.__fill_table(self.__cursor.fetchall())

    def __open_doctors(self):
        self.__create_table(("id", "name", "salary"))
        self.__current_table = "doctors"
        self.__cursor.execute("SELECT * FROM {};".format(self.__current_table))
        self.__fill_table(self.__cursor.fetchall())

    def __create_table(self, columns):
        self.__table.destroy()
        self.__table = ttk.Treeview(master=self.__table_frame)
        self.__table['columns'] = columns
        self.__table.column("#0", width=0, stretch=tk.NO)
        self.__table.heading("#0", text='')

        for widgets in self.__crud_frame.winfo_children():
            widgets.destroy()
        self.__textvariables.clear()

        for column in columns:
            self.__table.column(column, anchor=tk.CENTER, width=int(0.9 * self.__width / len(columns)))
            self.__table.heading(column, text=column, anchor=tk.CENTER)

        font = tkfont.Font(family="Times", size=14)
        size = int(self.__width * 0.85) // (font.measure("0") * len(columns))
        for i in range(1, len(columns)):
            tk.Label(master=self.__crud_frame, text=columns[i], font=font).grid(row=0, column=i-1)
            self.__textvariables.append(tk.StringVar())
            tk.Entry(master=self.__crud_frame, textvariable=self.__textvariables[-1], font=font, width=size) \
                .grid(row=1, column=i-1)

        tk.Button(master=self.__crud_frame, text="Add", background="#555", foreground="#ccc",
                  font="Times 11", width=size, command=self.__add_record).grid(row=1, column=len(columns), padx=20)

        self.__table.grid(row=0, column=0)
        self.__scrollbar.config(command=self.__table.yview)
        self.__table.config(yscrollcommand=self.__scrollbar.set)

    def __fill_table(self, records: list[tuple]):
        for record in records:
            self.__table.insert(parent='', index='end', iid=record[0], text='', values=record)

    def __add_record(self):
        try:
            record = tuple(map(lambda x: x.get().strip(), self.__textvariables))
            if '' in record:
                raise Exception("Fields cannot be empty")

            for textvariable in self.__textvariables:
                textvariable.set("")

            self.__cursor.execute("Select * FROM {} LIMIT 0;".format(self.__current_table))
            columns = [desc[0] for desc in self.__cursor.description]
            columns.pop(0)

            columns_list = "("
            for col in columns:
                columns_list += col + ", "
            columns_list = columns_list[:-2]
            columns_list += ")"

            self.__cursor.execute("INSERT INTO {}{} VALUES %s;".format(self.__current_table,
                                   columns_list), ((record, )))
            self.__connection.commit()

            self.__cursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(self.__current_table))
            record = self.__cursor.fetchall()[0]
            self.__table.insert(parent='', index='end', iid=record[0], text='', values=record)
        except Exception as e:
            messagebox.showinfo("Exception", e)

    def __remove_all(self):
        if len(self.__table.get_children()) == 0:
            messagebox.showinfo("", "Table is empty")
            return

        for record in self.__table.get_children():
            self.__table.delete(record)

        self.__cursor.execute("DELETE FROM {};".format(self.__current_table))
        self.__connection.commit()

    def __remove_selected(self):
        if len(self.__table.get_children()) == 0:
            messagebox.showinfo("", "Table is empty")
            return

        records = self.__table.selection()
        for record in records:
            self.__table.delete(record)

        self.__cursor.execute("DELETE FROM {} WHERE id IN %s;".format(self.__current_table), ((records, )))
        self.__connection.commit()