from tkinter import Tk
import view


class Controller:
    """Clase controlador que usaré para ejecutar la aplicación"""

    def __init__(self, root):
        """En el constructor indico que tomamos a root (de Tkinter) e instanciamos a "View", pasaremos dicho root como parametro para iniciar la aplicación"""
        self.root_controller = root
        self.display_view = view.View(self.root_controller)


def start_function():
    """Ejecuta la función"""
    if __name__ == "__main__":
        root_tk = Tk()
        Controller(root_tk)
        root_tk.mainloop()


start_function()
