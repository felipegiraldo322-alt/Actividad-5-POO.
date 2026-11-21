# Ejercicio 8.4. Cuadros de diálogo 

from enum import Enum
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ==========================================
# Enumeraciones: TipoCargo y TipoGénero
# ==========================================

class TipoCargo(Enum):
    """Dato enumerado que especifica el tipo de cargo que tiene un empleado."""
    DIRECTIVO = "Directivo"
    ESTRATÉGICO = "Estratégico"
    OPERATIVO = "Operativo"


class TipoGénero(Enum):
    """Dato enumerado que especifica el tipo de género que tiene un empleado."""
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


# ==========================================
# Clase: Empleado
# ==========================================

class Empleado:
    """
    Esta clase denominada Empleado modela un empleado de una empresa que tiene
    como atributos su nombre, apellidos, género, cargo, salario por día, otros
    ingresos, pagos por salud, aporte pensiones y días trabajados.
    """

    def __init__(
        self,
        nombre: str,
        apellidos: str,
        cargo: TipoCargo,
        género: TipoGénero,
        salario_día: float,
        días_trabajados: int,
        otros_ingresos: float,
        pagos_salud: float,
        aporte_pensiones: float,
    ):
        self._nombre = nombre
        self._apellidos = apellidos
        self._cargo = cargo
        self._género = género
        self._salario_día = salario_día
        self._días_trabajados = días_trabajados
        self._otros_ingresos = otros_ingresos
        self._pagos_salud = pagos_salud
        self._aporte_pensiones = aporte_pensiones

    def get_nombre(self) -> str:
        return self._nombre

    def get_apellidos(self) -> str:
        return self._apellidos

    def get_cargo(self) -> TipoCargo:
        return self._cargo

    def get_género(self) -> TipoGénero:
        return self._género

    def get_salario_día(self) -> float:
        return self._salario_día

    def get_días_trabajados(self) -> int:
        return self._días_trabajados

    def get_otros_ingresos(self) -> float:
        return self._otros_ingresos

    def get_pagos_salud(self) -> float:
        return self._pagos_salud

    def get_aporte_pensiones(self) -> float:
        return self._aporte_pensiones

    def calcular_nómina(self) -> float:
        """Calcula el salario mensual de un empleado."""
        return (
            (self._salario_día * self._días_trabajados)
            + self._otros_ingresos
            - self._pagos_salud
            - self._aporte_pensiones
        )


# ==========================================
# Clase: ListaEmpleados
# ==========================================

class ListaEmpleados:
    """
    Esta clase denominada ListaEmpleados define una lista de objetos Empleado
    y un total de la nómina de empleados.
    """

    def __init__(self):
        self.lista: list[Empleado] = []
        self.total_nómina: float = 0.0

    def agregar_empleado(self, empleado: Empleado) -> None:
        """Agrega un empleado a la lista de empleados."""
        self.lista.append(empleado)

    def calcular_total_nómina(self) -> float:
        """Calcula la nómina total mensual de la empresa."""
        self.total_nómina = 0.0
        for e in self.lista:
            self.total_nómina += e.calcular_nómina()
        return self.total_nómina

    def obtener_matriz(self) -> list[list[str]]:
        """Convierte los datos de la lista de empleados en una matriz."""
        self.total_nómina = 0.0
        datos: list[list[str]] = []
        for e in self.lista:
            nómina_empleado = e.calcular_nómina()
            datos.append([
                e.get_nombre(),
                e.get_apellidos(),
                str(nómina_empleado),
            ])
            self.total_nómina += nómina_empleado
        return datos

    def convertir_texto(self) -> str:
        """Convierte los datos de la lista de empleados a texto."""
        texto = ""
        for e in self.lista:
            texto += (
                f"Nombre = {e.get_nombre()}\n"
                f"Apellidos = {e.get_apellidos()}\n"
                f"Cargo = {e.get_cargo().name}\n"
                f"Género = {e.get_género().name}\n"
                f"Salario = ${e.get_salario_día()}\n"
                f"Días trabajados = {e.get_días_trabajados()}\n"
                f"Otros ingresos = ${e.get_otros_ingresos()}\n"
                f"Pagos saludo = ${e.get_pagos_salud()}\n"
                f"Aportes pensiones = ${e.get_aporte_pensiones()}\n"
                f"---------\n"
            )
        texto += f"Total nómina = ${self.calcular_total_nómina():.2f}"
        return texto


# ==========================================
# Clase: VentanaAgregarEmpleado
# ==========================================

class VentanaAgregarEmpleado(tk.Toplevel):
    """
    Define una ventana para ingresar los datos de un empleado y agregarlo
    a la lista de empleados.
    """

    def __init__(self, parent: tk.Misc, lista: ListaEmpleados):
        super().__init__(parent)
        self.lista = lista
        self.title("Agregar Empleado")
        self.geometry("300x400")
        self.resizable(False, False)
        self._centrar_ventana()
        self._inicio()

    def _centrar_ventana(self) -> None:
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _inicio(self) -> None:
        # Nombre
        tk.Label(self, text="Nombre:").place(x=20, y=20, width=135, height=23)
        self.campo_nombre = tk.Entry(self)
        self.campo_nombre.place(x=160, y=20, width=100, height=23)

        # Apellidos
        tk.Label(self, text="Apellidos:").place(x=20, y=50, width=135, height=23)
        self.campo_apellidos = tk.Entry(self)
        self.campo_apellidos.place(x=160, y=50, width=100, height=23)

        # Cargo (ComboBox)
        tk.Label(self, text="Cargo:").place(x=20, y=80, width=135, height=23)
        self.campo_cargo = ttk.Combobox(
            self,
            values=["Directivo", "Estratégico", "Operativo"],
            state="readonly",
        )
        self.campo_cargo.current(0)
        self.campo_cargo.place(x=160, y=80, width=100, height=23)

        # Género (RadioButtons)
        tk.Label(self, text="Género:").place(x=20, y=110, width=100, height=30)
        self.var_género = tk.StringVar(value="Masculino")
        tk.Radiobutton(
            self, text="Masculino", variable=self.var_género, value="Masculino"
        ).place(x=160, y=110, width=100, height=30)
        tk.Radiobutton(
            self, text="Femenino", variable=self.var_género, value="Femenino"
        ).place(x=160, y=140, width=100, height=30)

        # Salario por día
        tk.Label(self, text="Salario por día:").place(x=20, y=170, width=135, height=23)
        self.campo_salario_día = tk.Entry(self)
        self.campo_salario_día.place(x=160, y=170, width=100, height=23)

        # Días trabajados al mes (Spinbox)
        tk.Label(self, text="Días trabajados al mes:").place(
            x=20, y=200, width=135, height=23
        )
        self.var_días = tk.IntVar(value=30)
        self.campo_número_días = tk.Spinbox(
            self, from_=1, to=31, textvariable=self.var_días
        )
        self.campo_número_días.place(x=160, y=200, width=50, height=23)

        # Otros ingresos
        tk.Label(self, text="Otros ingresos:").place(x=20, y=230, width=135, height=23)
        self.campo_otros_ingresos = tk.Entry(self)
        self.campo_otros_ingresos.place(x=160, y=230, width=100, height=23)

        # Pagos por salud
        tk.Label(self, text="Pagos por salud:").place(x=20, y=260, width=135, height=23)
        self.campo_aportes_salud = tk.Entry(self)
        self.campo_aportes_salud.place(x=160, y=260, width=100, height=23)

        # Aportes pensiones
        tk.Label(self, text="Aportes pensiones:").place(
            x=20, y=290, width=135, height=23
        )
        self.campo_pensiones = tk.Entry(self)
        self.campo_pensiones.place(x=160, y=290, width=100, height=23)

        # Botones
        tk.Button(self, text="Agregar", command=self._añadir_empleado).place(
            x=20, y=320, width=100, height=23
        )
        tk.Button(self, text="Borrar", command=self._limpiar_campos).place(
            x=160, y=320, width=80, height=23
        )

    def _limpiar_campos(self) -> None:
        """Borra los campos ingresados en la ventana de agregar empleado."""
        self.campo_nombre.delete(0, tk.END)
        self.campo_apellidos.delete(0, tk.END)
        self.campo_salario_día.delete(0, tk.END)
        self.var_días.set(0)
        self.campo_otros_ingresos.delete(0, tk.END)
        self.campo_aportes_salud.delete(0, tk.END)
        self.campo_pensiones.delete(0, tk.END)

    def _añadir_empleado(self) -> None:
        """Valida los campos y agrega un empleado a la lista."""
        item_seleccionado = self.campo_cargo.get()
        if item_seleccionado == "Directivo":
            tipo_c = TipoCargo.DIRECTIVO
        elif item_seleccionado == "Estratégico":
            tipo_c = TipoCargo.ESTRATÉGICO
        else:
            tipo_c = TipoCargo.OPERATIVO

        if self.var_género.get() == "Masculino":
            tipo_g = TipoGénero.MASCULINO
        else:
            tipo_g = TipoGénero.FEMENINO

        try:
            valor1 = self.campo_nombre.get()
            valor2 = self.campo_apellidos.get()
            if not valor1.strip() or not valor2.strip():
                raise ValueError("Campos de texto vacíos")

            valor3 = float(self.campo_salario_día.get())
            valor4 = int(self.var_días.get())
            valor5 = float(self.campo_otros_ingresos.get())
            valor6 = float(self.campo_aportes_salud.get())
            valor7 = float(self.campo_pensiones.get())

            empleado = Empleado(
                valor1, valor2, tipo_c, tipo_g, valor3, valor4, valor5, valor6, valor7
            )
            self.lista.agregar_empleado(empleado)
            messagebox.showinfo("Mensaje", "El empleado ha sido agregado", parent=self)
            self._limpiar_campos()
        except Exception:
            messagebox.showerror(
                "Error", "Campo nulo o error en formato de numero", parent=self
            )


# ==========================================
# Clase: VentanaNómina
# ==========================================

class VentanaNómina(tk.Toplevel):
    """
    Define una interfaz gráfica que permitirá consultar la lista de empleados
    y la nómina total.
    """

    def __init__(self, parent: tk.Misc, lista: ListaEmpleados):
        super().__init__(parent)
        self.lista = lista
        self.title("Nómina de Empleados")
        self.geometry("350x250")
        self.resizable(False, False)
        self._centrar_ventana()
        self._inicio()

    def _centrar_ventana(self) -> None:
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _inicio(self) -> None:
        tk.Label(self, text="Lista de empleados:").place(x=20, y=10, width=135, height=23)

        datos = self.lista.obtener_matriz()
        titulos = ("NOMBRE", "APELLIDOS", "SUELDO")

        tabla = ttk.Treeview(self, columns=titulos, show="headings")
        for col in titulos:
            tabla.heading(col, text=col)
            tabla.column(col, width=100, anchor=tk.W)

        for fila in datos:
            tabla.insert("", tk.END, values=fila)

        tabla.place(x=20, y=50, width=310, height=100)

        tk.Label(
            self, text=f"Total nómina mensual = $ {self.lista.total_nómina:.2f}"
        ).place(x=20, y=160, width=250, height=23)


# ==========================================
# Clase: VentanaPrincipal
# ==========================================

class VentanaPrincipal(tk.Tk):
    """
    Define una interfaz gráfica principal que permitirá gestionar la nómina
    de empleados.
    """

    def __init__(self):
        super().__init__()
        self.empleados = ListaEmpleados()
        self.title("Nómina")
        self.geometry("280x380")
        self.resizable(False, False)
        self._centrar_ventana()
        self._inicio()

    def _centrar_ventana(self) -> None:
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _inicio(self) -> None:
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(
            label="Agregar empleado", command=self._abrir_agregar_empleado
        )
        menu_opciones.add_command(
            label="Calcular nómina", command=self._abrir_ventana_nómina
        )
        menu_opciones.add_separator()
        menu_opciones.add_command(
            label="Guardar archivo", command=self._guardar_archivo
        )
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

    def _abrir_agregar_empleado(self) -> None:
        VentanaAgregarEmpleado(self, self.empleados)

    def _abrir_ventana_nómina(self) -> None:
        VentanaNómina(self, self.empleados)

    def _guardar_archivo(self) -> None:
        directorio_elegido = filedialog.askdirectory(parent=self, title="Seleccionar carpeta")
        if directorio_elegido:
            try:
                contenido = self.empleados.convertir_texto()
                ruta_archivo = f"{directorio_elegido}/Nómina.txt"
                with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                    archivo.write(contenido)

                nombre_carpeta = directorio_elegido.split("/")[-1].split("\\")[-1]
                messagebox.showinfo(
                    "Mensaje",
                    f"El archivo de la nómina Nómina.txt se ha creado en {nombre_carpeta}",
                    parent=self,
                )
            except Exception as e:
                print(e)


# ==========================================
# Clase / Punto de entrada: Principal
# ==========================================

class Principal:
    """Define el punto de ingreso al programa de la nómina de empleados."""

    @staticmethod
    def main(args: list[str] | None = None) -> None:
        mi_ventana_principal = VentanaPrincipal()
        mi_ventana_principal.resizable(False, False)
        mi_ventana_principal.mainloop()


if __name__ == "__main__":
    Principal.main()