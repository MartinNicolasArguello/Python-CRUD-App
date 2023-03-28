from model import Model
from tkinter import *
from tkinter import ttk
import observers
import re

"""En este módulo se encuentra nuestra vista, que sera instanciada en el controlador para iniciar la aplicación. Es aquí también donde se instancian las demás clases importantes, el modelo y los observadores."""


class View:
    def __init__(self, window):
        self.root = window
        self.root.title("Trabajo integrador final")
        self.root.geometry("1100x700")
        self.root.iconbitmap("icon.ico")
        """Se instancia el modelo."""
        self.obj = Model()
        """Se instancia el observador, pasando el modelo(que es nuestro observable) como parámetro."""
        self.model_observer = observers.Observer(self.obj)
        """Se agrega el observador al modelo (observable)"""
        self.obj.add_observer(self.model_observer)
        # Header

        self.title = Label(
            self.root,
            text="Olimpus Gym",
            background="#231F20",
            foreground="#8E793E",
            font="times 35 bold ",
            height="2",
        )
        self.title.pack(side="top", fill="x")

        # Notebook

        self.notebook = ttk.Notebook(width=1100, height=150)

        self.tab1 = Frame(self.notebook)
        self.tab2 = Frame(self.notebook)

        self.notebook.add(self.tab1, text="Add/Delete")
        self.notebook.add(self.tab2, text="Modify")
        self.notebook.pack(expand="true", fill="both")

        # TAB 1
        self.invisible_container = Frame
        self.form_container = Frame(self.root)
        self.form_container.pack(in_=self.tab1, side=LEFT)
        self.button_container = Frame(self.root)
        self.button_container.pack(in_=self.tab1)
        self.add_btn = Button(
            self.root,
            text="ADD",
            background="#231F20",
            foreground="#8E793E",
            height=5,
            width=10,
            font="times 20 bold",
            command=lambda: self.obj.insert(
                self.root,
                self.tree,
                self.dni_add.get(),
                self.lastname_add.get(),
                self.class_add.get(),
                self.plan_add.get(),
                self.success,
                self.button_container,
                self.dni_add,
                self.lastname_add,
                self.class_add,
                self.plan_add,
                self.del_btn,
            ),
            state="disabled",
        )

        self.add_btn.grid(in_=self.button_container, row=0, column=0)

        self.del_btn = Button(
            self.root,
            text="DEL",
            background="#231F20",
            foreground="#8E793E",
            height=5,
            width=10,
            font="times 20 bold",
            command=lambda: self.obj.delete(
                self.tree, self.del_btn, self.root, self.success, self.button_container
            ),
            state="disabled",
        )

        self.del_btn.grid(in_=self.button_container, row=0, column=1)

        self.dni_add, self.lastname_add, self.class_add, self.plan_add = (
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
        )

        def add_btn_monitor(*args):
            dni, lastname, class_, plan = (
                self.dni_add.get(),
                self.lastname_add.get(),
                self.class_add.get(),
                self.plan_add.get(),
            )
            if dni and lastname and class_ != "None" and plan != "None":

                self.add_btn.config(state="normal")
            else:

                self.add_btn.config(state="disabled")

        self.dni_add.trace("w", add_btn_monitor)
        self.lastname_add.trace("w", add_btn_monitor)
        self.class_add.trace("w", add_btn_monitor)
        self.plan_add.trace("w", add_btn_monitor)

        self.class_add.set(None)
        self.plan_add.set(None)

        self.add_dni = Label(text="DNI", font="times 10 italic", width=20)
        self.add_dni.grid(in_=self.form_container, row=0, column=0, sticky=W)
        self.entry_dni = Entry(self.root, textvariable=self.dni_add, width=20)
        self.entry_dni.grid(in_=self.form_container, row=0, column=1)
        self.add_lastname = Label(text="Last name", font="times 10 italic", width=20)
        self.add_lastname.grid(in_=self.form_container, row=1, column=0)
        self.entry_lastname = Entry(self.root, textvariable=self.lastname_add, width=20)
        self.entry_lastname.grid(in_=self.form_container, row=1, column=1, sticky=W)

        self.add_class = Label(text="Class", font="times 10 italic", width=20)
        self.add_class.grid(in_=self.form_container, row=3, column=0)

        Radiobutton(
            text="Weight Machines", variable=self.class_add, value="Weight Machines"
        ).grid(in_=self.form_container, row=2, column=1, sticky=W)
        Radiobutton(text="Spinning", variable=self.class_add, value="Spinning").grid(
            in_=self.form_container, row=3, column=1, sticky=W
        )

        Radiobutton(text="Cross Fit", variable=self.class_add, value="Cross Fit").grid(
            in_=self.form_container, row=4, column=1, sticky=W
        )
        add_plan = Label(text="Plan", font="times 10 italic", width=20)
        add_plan.grid(in_=self.form_container, row=3, column=2)

        Radiobutton(
            text="1 month ($300)", variable=self.plan_add, value="One month"
        ).grid(in_=self.form_container, row=2, column=3, sticky=W)
        Radiobutton(
            text="3 months ($700)", variable=self.plan_add, value="Three months"
        ).grid(in_=self.form_container, row=3, column=3, sticky=W)

        Radiobutton(
            text="6 months ($1000)", variable=self.plan_add, value="Semestral"
        ).grid(in_=self.form_container, row=4, column=3, sticky=W)

        self.success = Label(
            self.root, text="Success!", foreground="#AD974F", font="times 15 bold"
        )

        # TAB 2
        self.modify_container1 = Frame(self.root, background="#231F20")
        self.modify_container1.pack(in_=self.tab2, pady=10)
        self.modify_container2 = Frame(self.root)

        def verify_search_monitor(*args):
            self.modify_search_button.config(state="disabled")
            num = self.searched_dni_modify.get()
            dni_pattern = re.compile("^[0-9]{7,8}$")
            if re.match(dni_pattern, num):
                self.modify_search_button.config(state="normal")

        def submit_monitor(*args):
            self.submit_changes_btn.config(state="disabled")
            var1 = self.new_class.get()
            var2 = self.new_plan.get()
            if var1 and var2:
                self.submit_changes_btn.config(state="normal")

        self.searched_dni_modify = StringVar()
        self.searched_dni_modify.trace("w", verify_search_monitor)
        self.new_class = StringVar()
        self.new_class.trace("w", submit_monitor)
        self.new_plan = StringVar()
        self.new_plan.trace("w", submit_monitor)
        self.search_dni_modify = Label(
            text="DNI",
            font="times 10 italic",
            width=10,
            background="#231F20",
            foreground="#8E793E",
        )
        self.search_dni_modify.grid(
            in_=self.modify_container1, row=0, column=0, sticky=W
        )
        self.entry_dni_modify = Entry(
            self.root, textvariable=self.searched_dni_modify, width=20
        )
        self.entry_dni_modify.grid(in_=self.modify_container1, row=0, column=1)

        self.modify_label5 = Label(width=20)
        self.modify_label6 = Label(width=20)
        self.modify_label7 = Label(width=20)
        self.modify_label8 = Label(width=20)
        self.tree = ttk.Treeview(self.root)
        self.success2 = Label(
            self.root,
            text="Changes submited",
            foreground="#AD974F",
            font="times 12 bold",
        )
        self.error = Label(
            self.root, text="No Changes", foreground="#f04b4c", font="times 15 bold"
        )
        self.modify_search_button = Button(
            self.root,
            text="Search",
            width=10,
            background="#231F20",
            foreground="#8E793E",
            font="times 10 bold",
            command=lambda: self.obj.verify_search(
                self.searched_dni_modify.get(),
                self.tab2,
                self.modify_container2,
                self.modify_label5,
                self.modify_label6,
                self.modify_label7,
                self.modify_label8,
            ),
            state="disabled",
        )
        self.modify_search_button.grid(in_=self.modify_container1, row=0, column=2)

        self.modify_label1 = Label(
            text="DNI", width=20, background="#231F20", foreground="#8E793E"
        )
        self.modify_label1.grid(
            in_=self.modify_container2,
            row=0,
            column=0,
        )
        self.modify_label2 = Label(
            text="Lastname", width=20, background="#231F20", foreground="#8E793E"
        )
        self.modify_label2.grid(in_=self.modify_container2, row=0, column=1)
        self.modify_label3 = Label(
            text="Selected Class", width=20, background="#231F20", foreground="#8E793E"
        )
        self.modify_label3.grid(in_=self.modify_container2, row=0, column=2)
        self.modify_label4 = Label(
            text="Selected Plan", width=20, background="#231F20", foreground="#8E793E"
        )
        self.modify_label4.grid(in_=self.modify_container2, row=0, column=3)

        self.modify_label5.grid(
            in_=self.modify_container2,
            row=1,
            column=0,
        )

        self.modify_label6.grid(in_=self.modify_container2, row=1, column=1)

        self.modify_label7.grid(in_=self.modify_container2, row=1, column=2)

        self.modify_label8.grid(in_=self.modify_container2, row=1, column=3)
        self.modify_label11 = Label(
            text="New Class", width=20, background="#231F20", foreground="#EAEAEA"
        )
        self.modify_label11.grid(in_=self.modify_container2, row=2, column=2)
        self.modify_label12 = Label(
            text="New Plan", width=20, background="#231F20", foreground="#EAEAEA"
        )
        self.modify_label12.grid(in_=self.modify_container2, row=2, column=3)

        self.modify_combo1 = ttk.Combobox(
            self.root, textvariable=self.new_class, state="readonly"
        )
        self.modify_combo1.grid(in_=self.modify_container2, row=3, column=2)
        self.modify_combo1["values"] = ("Weight Machines", "Spinning", "Crossfit")
        self.modify_combo2 = ttk.Combobox(
            self.root, textvariable=self.new_plan, state="readonly"
        )
        self.modify_combo2.grid(in_=self.modify_container2, row=3, column=3)
        self.modify_combo2["values"] = ("1 Month", "3 Months", "6 Months")
        self.submit_changes_btn = Button(
            self.root,
            text="Submit Changes",
            width=19,
            background="#EAEAEA",
            foreground="#8E793E",
            font="times 10 bold",
            state="disabled",
            command=lambda: self.obj.submit_changes(
                self.modify_label5.cget("text"),
                self.new_class.get(),
                self.new_plan.get(),
                self.modify_label7.cget("text"),
                self.modify_label8.cget("text"),
                self.tree,
                self.modify_container2,
                self.entry_dni_modify,
                self.modify_combo1,
                self.modify_combo2,
                self.del_btn,
                self.success2,
                self.modify_container1,
                self.root,
                self.error,
            ),
        )
        self.submit_changes_btn.grid(in_=self.modify_container2, row=4, column=3)

        self.searched_dni_modify.trace("w", verify_search_monitor)
        self.new_class.trace("w", submit_monitor)
        self.new_plan.trace("w", submit_monitor)
        # Tree menu

        self.menu_container = Frame(self.root)
        self.menu_container.pack(side=TOP)
        self.display_label = Label(
            self.root,
            text="Display",
            font="times 20 bold ",
            foreground="#8E793E",
        )
        self.display_label.pack(in_=self.menu_container, side=TOP, fill=X)
        self.display1 = Button(
            self.root,
            text="All",
            foreground="#8E793E",
            background="#231F20",
            command=lambda: self.obj.update_treeview(self.tree, self.del_btn),
        )
        self.display1.pack(in_=self.menu_container, side=LEFT)
        self.display2 = Button(
            self.root,
            text="Weight Machines",
            background="#231F20",
            foreground="#8E793E",
            command=lambda: self.obj.display_weights(self.tree, self.del_btn),
        )
        self.display2.pack(in_=self.menu_container, side=LEFT)
        self.display3 = Button(
            self.root,
            text="Spinning",
            background="#231F20",
            foreground="#8E793E",
            command=lambda: self.obj.display_spinning(self.tree, self.del_btn),
        )
        self.display3.pack(in_=self.menu_container, side=LEFT)
        self.display4 = Button(
            self.root,
            text="Crossfit",
            background="#231F20",
            foreground="#8E793E",
            command=lambda: self.obj.display_crossfit(self.tree, self.del_btn),
        )
        self.display4.pack(in_=self.menu_container, side=LEFT)

        # Tree

        # self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("Lastname", "Class", "Plan")
        self.tree.column("#0", width=90, anchor=CENTER)
        self.tree.column("Lastname", width=200, anchor=CENTER)
        self.tree.column("Class", width=200, anchor=CENTER)
        self.tree.column("Plan", width=200, anchor=CENTER)
        self.tree.heading("#0", text="DNI")
        self.tree.heading("Lastname", text="Member Lastname")
        self.tree.heading("Class", text="Class")
        self.tree.heading("Plan", text="Plan")
        self.tree.pack(expand="true", fill="both")

        def del_btn_monitor(event):
            obj = self.tree.selection()
            if obj:
                self.del_btn.config(state="normal")

        self.tree.bind("<ButtonRelease-1>", del_btn_monitor)
