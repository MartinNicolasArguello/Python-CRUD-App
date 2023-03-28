"""El patrón observador lo apliqué creando sus clases en un módulo aparte, estas son ..."""


class Observer:
    """La clase “observador” toma a su observable, el modelo, como parámetro de constructor, ya que desde ahí podrá acceder a la base de datos. Desde ahí con “publish()” ordena la información, imprime la clase con mayor número de miembros y chequea si las otras 2 alcanzaron el objetivo de 5 miembros."""

    def __init__(self, target):
        self.target = target

    def publish(self):
        print("Starting observer's report")
        members_counted = {"Spinning": 0, "Weight Machine": 0, "Cross Fit": 0}
        sql = "SELECT * FROM test"
        con = self.target.create_base()
        cursor = con.cursor()
        data = cursor.execute(sql)
        result = data.fetchall()
        for member in result:
            match member[2]:
                case "Spinning":
                    members_counted["Spinning"] += 1
                case "Weight Machines":
                    members_counted["Weight Machine"] += 1
                case "Cross Fit":
                    members_counted["Cross Fit"] += 1
        higher_class = max(members_counted, key=members_counted.get)

        print(
            "%s is our most attended class with %d current members attending"
            % (higher_class, members_counted[higher_class])
        )
        members_counted.pop(higher_class)
        for entry in members_counted:
            if members_counted[entry] < 5:
                print(
                    "Our %s class is still behind our 5 members attendance goal with only %d current members attending"
                    % (entry, members_counted[entry])
                )
            else:
                print(
                    "Our %s class reached our 5 attendance goal, with %d current members attending"
                    % (entry, members_counted[entry])
                )


class Observed:
    """La clase “observable” que tiene dos métodos, uno para “agregar” observadores y otro para notificar a su observador  para que éste ejecute su método “publish”."""

    def add_observer(self, observer):
        self.observer = observer

    def notify(self):

        if self.observer:
            self.observer.publish()


"""La clase “Model” es instanciada en la clase “View” y  hereda de “Observed”, entonces el modelo puede usar el método heredado “notify” al final de cada operación que altere el número de miembros para que el observador, que es también instanciado dentro de view y “agregado” al modelo (el observable), haga su informe con “publish()”
"""
