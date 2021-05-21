from dbworker import DBWorker
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tm
import tkinter as tk



config = {"database": {"host": "localhost",
                       "port": 5432,
                       "dbname": "postgres",
                       "user": "postgres",
                       "password": "root"
                       }}

# config = {"database": {"host": "localhost",
#                        "port": 5432,
#                        "dbname": "postgres",
#                        "user": "misitizer",
#                        "password": "Passw0rd"
#                        }}
#
# config = {"database": {"host": "localhost",
#                        "port": 5432,
#                        "dbname": "postgres",
#                        "user": "sanya",
#                        "password": "sosi"
#                        }}
db_worker = DBWorker(config)

root = Tk()
root.title('DB')
root.geometry('800x600')


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
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


def sql_select(query: str) -> None:
    columns, res = db_worker.select(query)
    print(columns)
    result = f'{str(columns)[1:-1]}\n'
    print(res[1])
    for line in res:
        result += str(line)[1:-1] + '\n'
    return result


def give_some_grants():
    user = entry_grant_username.get()
    table = entry_grant_table.get()
    subquery = ''
    grants = {0: 'SELECT', 1: 'INSERT', 2: 'UPDATE', 3: 'DELETE'}
    for i in range(len(variables)):
        if variables[i].get() == 1:
            subquery += grants[i] + ','

    query = f'grant {subquery[:-1]} on {table} to {user}'
    if db_worker.exec_command(query):
        tm.showinfo('Успех', f'Привелегия для {user} добавлена.')
    else:
        tm.showerror('Ошибка', 'Ошибка БД, обратитесь к администратору.')


def execute_select():
    query = sql_in.get(1.0, END)
    sql_result = Table(f1, headings=db_worker.select(query)[0], rows=db_worker.select(query)[1])
    sql_result.place(x=10, y=300)


def login_btn_clicked():
    username = entry_username.get()
    password = entry_password.get()
    password1 = entry_password1.get()
    if password == password1:
        db_worker.exec_command(f'''create user {username} with password \'{password}\'''')
        tm.showinfo('Успех', 'Пользователь создан.')
    else:
        tm.showerror('Ошибка', 'Разные пароли.')


def execute_insert():
    query = sql_insert.get(1.0, END)
    if db_worker.exec_command(query):
        tm.showinfo('Успех', 'Запись добавлена')
    else:
        tm.showerror('Ошибка', 'Ошибка при заполнении. Проверьте консоль.')


nb = ttk.Notebook(root)
nb.pack(fill='both', expand='yes')

f1 = Frame(nb)
f2 = Frame(nb)
f3 = Frame(nb)
f4 = Frame(nb)

nb.add(f1, text='SQL Select')
nb.add(f2, text='SQL Insert/Update')
nb.add(f3, text='Grants')
nb.add(f4, text='Create User')

label = Label(f1, text='Введи SQL запрос: ')
label_out = Label(f1, text='Результат запроса: ')
sql_in = Text(f1, width=80, height=10)
exec_select = Button(f1, text="Execute", command=execute_select)
# sql_result = Table(root, headings=db_worker.select('select * from public.d_tickettype')[0], rows=db_worker.select('select * from public.d_tickettype')[1])


sql_in.place(x=10, y=60)
label_out.place(x=10, y=280)
# sql_result.place(x=10, y=300)
label.place(x=10, y=40)
exec_select.place(x=10, y=230)

label_insert = Label(f2, text='Введи SQL запрос: ')
sql_insert = Text(f2, width=80, height=10)
exec_insert = Button(f2, text="Execute", command=execute_insert)

label_insert.place(x=10, y=40)
exec_insert.place(x=10, y=230)
sql_insert.place(x=10, y=60)

l_grant_username = Label(f3, text="Username: ")
entry_grant_username = Entry(f3)
l_grant_table = Label(f3, text="Table: ")
entry_grant_table = Entry(f3)
add_grants = Button(f3, text="Grant", command=give_some_grants)

variables = [BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar()]

w1 = Checkbutton(f3, text='SELECT', variable=variables[0])
w2 = Checkbutton(f3, text='INSERT', variable=variables[1])
w3 = Checkbutton(f3, text='UPDATE', variable=variables[2])
w4 = Checkbutton(f3, text='DELETE', variable=variables[3])

l_grant_username.grid(row=0, sticky=E)
l_grant_table.grid(row=1, sticky=E)

entry_grant_username.grid(row=0, column=1)
entry_grant_table.grid(row=1, column=1)
add_grants.place(x=100, y=120)

w1.place(x=100, y=40)
w2.place(x=100, y=60)
w3.place(x=100, y=80)
w4.place(x=100, y=100)

label_username = Label(f4, text="Username: ")
label_password = Label(f4, text="Password: ")
label_password1 = Label(f4, text="Repeat: ")
entry_username = Entry(f4)
entry_password = Entry(f4, show="*")
entry_password1 = Entry(f4, show="*")

label_username.grid(row=0, sticky=E)
label_password.grid(row=1, sticky=E)
label_password1.grid(row=2, sticky=E)

entry_username.grid(row=0, column=1)
entry_password.grid(row=1, column=1)
entry_password1.grid(row=2, column=1)

logbtn = Button(f4, text="Create", command=login_btn_clicked)
logbtn.grid(columnspan=2)

root.mainloop()
