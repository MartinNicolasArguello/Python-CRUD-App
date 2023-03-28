from tkinter import messagebox
from tkinter import *
import sqlite3
import observers

# import datetime
from datetime import datetime
import re


"""En este módulo se encuentra toda la lógica de la aplicación dentro de una clase "Model", que hereda de la clase observable, de esta que obtenemos el método "notify" que se usa al final de cada operación para que los observadores realicen su función"""


class Model(observers.Observed):
    def __init__(self):
        try:
            con = sqlite3.connect("mibase.db")
            cursor = con.cursor()
            # sql = """CREATE TABLE test
            #             (dni varchar(20) PRIMARY KEY,
            #             lastname varchar(20) NOT NULL,
            #             class varchar(20) NOT NULL,
            #             plan varchar(20) NOT NULL)
            #             """
            # cursor.execute(sql)
            # con.commit()
        except:
            print("error?")

    def decorator(function):
        """El decorador “envuelve” a las funciones que modifican entradas en la base de datos, su única función es “avisar” por consola de la modificación, imprimiendo desde que función fue llamado y a que hora."""
        currentDateAndTime = datetime.now()
        currentTime = currentDateAndTime.strftime("%H:%M:%S")

        def inner(*args, **kwargs):

            print(
                "Called at %s " % currentTime
                + " from function: "
                + function.__name__.upper()
            )
            val = function(*args, **kwargs)
            return val

        return inner

    def create_base(
        self,
    ):
        con = sqlite3.connect("mibase.db")
        return con

    def add_success(self, row, column, root, success, button_container):
        """Presenta un mensaje temporal (1 segundo de duración) informando el éxito de la operación "Insert" o "Delete", dependiendo de cual de estas dos funciones llame al método, será la ubicación del mensaje temporal"""
        success.grid(in_=button_container, row=row, column=column)
        root.after(1000, success.grid_forget)

    @decorator
    def insert(
        self,
        root,
        tree,
        dni,
        lastname,
        class_,
        plan,
        success,
        button_container,
        dni_add,
        lastname_add,
        class_add,
        plan_add,
        del_btn,
    ):
        """Se encarga de los registros a la base de datos, usando validadores para que la información tenga el formato deseado, y verificando de que el DNI (que uso como primary key) ya no se encuentre en uso."""
        dni_pattern = re.compile("^[0-9]{7,8}$")
        lastname_pattern = re.compile("^([A-Z][a-z]{0,20})([\s][A-Z][a-z]{0,20})?$")
        if re.match(dni_pattern, dni) and re.match(lastname_pattern, lastname):
            con = self.create_base()
            cursor = con.cursor()
            data = (dni, lastname, class_, plan)
            sql = "INSERT INTO test (dni, lastname, class, plan) VALUES(?, ?, ?, ?);"
            try:
                cursor.execute(sql, data)
                con.commit()
                self.update_treeview(tree, del_btn)
                self.add_success(1, 0, root, success, button_container)
                self.reset_add_form(dni_add, lastname_add, class_add, plan_add)
                self.notify()
            except:
                messagebox.showinfo("error", "Repeated DNI")
        else:
            if not re.match(dni_pattern, dni):
                messagebox.showinfo("error", "Invalid DNI")
            if not re.match(lastname_pattern, lastname):
                messagebox.showinfo("error", "Invalid Last Name")

    @decorator
    def delete(self, tree, del_btn, root, success, button_container):
        """Se encarga de eliminar entradas de la base de datos. permite eliminar mas de un elemento por operación."""
        value = tree.selection()
        if len(tree.selection()) > 1:
            for selection in value:
                item = tree.item(selection)
                dni = item["text"]
                data = (dni,)
                sql = "DELETE FROM test WHERE dni =?;"
                con = self.create_base()
                cursor = con.cursor()
                cursor.execute(sql, data)
                con.commit()
                tree.delete(selection)
                del_btn.config(state="disabled")
                self.add_success(1, 1, root, success, button_container)
            self.notify()
        else:
            item = tree.item(value)
            dni = item["text"]
            data = (dni,)
            sql = "DELETE FROM test WHERE dni =?;"
            con = self.create_base()
            cursor = con.cursor()
            cursor.execute(sql, data)
            con.commit()
            tree.delete(value)
            del_btn.config(state="disabled")
            self.add_success(1, 1, root, success, button_container)
            self.notify()

    @decorator
    def submit_changes(
        self,
        var1,
        var2,
        var3,
        modify_label7,
        modify_label8,
        tree,
        modify_container2,
        entry_dni_modify,
        modify_combo1,
        modify_combo2,
        del_btn,
        success2,
        modify_container1,
        root,
        error,
    ):
        """Se encarga de modificar entradas ya existentes en la base de datos."""
        if var2 == modify_label7 and var3 == modify_label8:
            self.modify_error(error, modify_container2, root)
        else:
            con = self.create_base()
            cursor = con.cursor()
            sql = "UPDATE test SET class = ?, plan = ? WHERE dni = ?;"
            data = (var2, var3, var1)
            cursor.execute(sql, data)
            con.commit()
            self.update_treeview(tree, del_btn)
            self.reset_mod_form(
                modify_container2, entry_dni_modify, modify_combo1, modify_combo2
            )
            self.modify_success(success2, modify_container1, root)
            self.notify()

    def reset_add_form(self, dni_add, lastname_add, class_add, plan_add):
        dni_add.set(""),
        lastname_add.set(""),
        class_add.set(None),
        plan_add.set(None)

    def verify_search(
        self,
        searched_dni,
        tab2,
        modify_container2,
        modify_label5,
        modify_label6,
        modify_label7,
        modify_label8,
    ):
        """Comprueba si el DNI pertenece a un usuario."""
        sql = "SELECT * FROM test WHERE dni=?;"
        con = self.create_base()
        cursor = con.cursor()
        data = cursor.execute(sql, (searched_dni,)).fetchall()
        if data:
            self.display_form(
                data,
                tab2,
                modify_container2,
                modify_label5,
                modify_label6,
                modify_label7,
                modify_label8,
            )
        else:
            messagebox.showinfo("error", "Invalid DNI")

    def display_form(
        self,
        data,
        tab2,
        modify_container2,
        modify_label5,
        modify_label6,
        modify_label7,
        modify_label8,
    ):

        """Una vez verificado el DNI, esta función presenta el formulario para modificar el usuario."""
        modify_container2.pack(in_=tab2, pady=10)
        modify_label5.config(text=data[0][0])
        modify_label6.config(text=data[0][1])
        modify_label7.config(text=data[0][2])
        modify_label8.config(text=data[0][3])

    def reset_mod_form(
        self, modify_container2, entry_dni_modify, modify_combo1, modify_combo2
    ):
        """Después de realizada la operación, vuelve a esconder el formulario para modificar."""
        modify_container2.forget()
        entry_dni_modify.delete(0, "end")
        modify_combo1.set("")
        modify_combo2.set("")

    def update_treeview(self, tree, del_btn):
        """Actualiza la información que presenta el treeview, las restantes funciones sirven para mostrar solo los miembros pertenecientes a la clase correspondiente."""
        records = tree.get_children()
        for element in records:
            tree.delete(element)
        sql = "SELECT * FROM test ORDER BY lastname DESC"
        con = self.create_base()
        cursor = con.cursor()
        data = cursor.execute(sql)
        result = data.fetchall()
        for member in result:
            tree.insert("", 0, text=member[0], values=(member[1], member[2], member[3]))
        del_btn.config(state="disabled")

    def display_weights(self, tree, del_btn):
        records = tree.get_children()
        for element in records:
            tree.delete(element)
        sql = "SELECT * FROM test WHERE class='Weight Machines' ORDER BY lastname DESC"
        con = self.create_base()
        cursor = con.cursor()
        data = cursor.execute(sql)
        result = data.fetchall()
        for member in result:
            tree.insert("", 0, text=member[0], values=(member[1], member[2], member[3]))
        del_btn.config(state="disabled")

    def display_crossfit(self, tree, del_btn):
        records = tree.get_children()
        for element in records:
            tree.delete(element)
        sql = "SELECT * FROM test WHERE class='Cross Fit' ORDER BY lastname DESC"
        con = self.create_base()
        cursor = con.cursor()
        data = cursor.execute(sql)
        result = data.fetchall()
        for member in result:
            tree.insert("", 0, text=member[0], values=(member[1], member[2], member[3]))
        del_btn.config(state="disabled")

    def display_spinning(self, tree, del_btn):
        records = tree.get_children()
        for element in records:
            tree.delete(element)
        sql = "SELECT * FROM test WHERE class='Spinning' ORDER BY lastname DESC"
        con = self.create_base()
        cursor = con.cursor()
        data = cursor.execute(sql)
        result = data.fetchall()
        for member in result:
            tree.insert("", 0, text=member[0], values=(member[1], member[2], member[3]))
        del_btn.config(state="disabled")

    def modify_success(self, success2, modify_container1, root):
        """Se encarga de presentar un mensaje temporal (1 segundo de duración) informando el éxito de la operación "Modify" """
        success2.grid(
            in_=modify_container1, row=1, column=0, columnspan=3, sticky=W + E
        )
        root.after(1500, success2.grid_forget)

    def modify_error(self, error, modify_container2, root):
        """Se encarga de presentar un mensaje temporal (1 segundo de duración) informando un fallo de la operación "Modify" """
        error.grid(in_=modify_container2, row=5, column=3)
        root.after(1500, error.grid_forget)
