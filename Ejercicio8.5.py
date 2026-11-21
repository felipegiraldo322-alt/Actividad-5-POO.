# Ejercicio 8.5. Gestión de contenidos 

from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Clase huésped
class Huésped:
    """
    Esta clase denominada Huésped define un huésped del hotel que
    ocupará una determinada habitación por ciertos días.
    """

    def __init__(self, nombres: str, apellidos: str, documento_identidad: int):
        self._nombres = nombres
        self._apellidos = apellidos
        self._documento_identidad = documento_identidad
        self._fecha_ingreso: datetime | None = None
        self._fecha_salida: datetime | None = None

    def set_fecha_salida(self, fecha: datetime) -> None:
        self._fecha_salida = fecha

    def set_fecha_ingreso(self, fecha: datetime) -> None:
        self._fecha_ingreso = fecha

    def get_fecha_ingreso(self) -> datetime | None:
        return self._fecha_ingreso

    def obtener_días_alojamiento(self) -> int:
        """Calcula la cantidad de días de alojamiento del huésped."""
        if self._fecha_ingreso is None or self._fecha_salida is None:
            return 0
        diferencia = self._fecha_salida - self._fecha_ingreso
        return int(diferencia.total_seconds() // 86400)

# Clase habitación
class Habitación:
    """
    Esta clase denominada Habitación define una habitación de un hotel
    a ser ocupada y desocupada por un huésped.
    """

    def __init__(self, número_habitación: int, disponible: bool, precio_día: float):
        self._número_habitación = número_habitación
        self._disponible = disponible
        self._precio_día = precio_día
        self._huésped: Huésped | None = None

    def get_número_habitación(self) -> int:
        return self._número_habitación

    def get_disponible(self) -> bool:
        return self._disponible

    def get_precio_día(self) -> float:
        return self._precio_día

    def get_huésped(self) -> Huésped | None:
        return self._huésped

    def set_huésped(self, huésped: Huésped | None) -> None:
        self._huésped = huésped

    def set_disponible(self, disponible: bool) -> None:
        self._disponible = disponible

# Clase hotel
class Hotel:
    """
    Esta clase denominada Hotel define un hotel que contiene diez
    habitaciones a ser ocupadas y liberadas por diferentes huéspedes en
    fechas determinadas.
    """

    lista_habitaciones: list[Habitación] = []

    def __init__(self):
        Hotel.lista_habitaciones = []
        for i in range(1, 11):
            precio = 120000.0 if i <= 5 else 160000.0
            Hotel.lista_habitaciones.append(Habitación(i, True, precio))

    def buscar_fecha_ingreso_habitación(self, número: int) -> str:
        """Dado un número de habitación, busca la fecha de ingreso del huésped."""
        for habitación in Hotel.lista_habitaciones:
            if habitación.get_número_habitación() == número:
                huésped = habitación.get_huésped()
                if huésped and huésped.get_fecha_ingreso():
                    return huésped.get_fecha_ingreso().strftime("%Y/%m/%d")
        return ""

    def buscar_habitación_ocupada(self, número: int) -> bool:
        """Dado un número de habitación, devuelve si está ocupada o no."""
        for habitación in Hotel.lista_habitaciones:
            if (
                habitación.get_número_habitación() == número
                and not habitación.get_disponible()
            ):
                return True
        return False

# Clase VentanaIngreso
class VentanaIngreso(tk.Toplevel):
    """
    Define una ventana que permite ingresar los datos del huésped que
    tomará una habitación previamente seleccionada.
    """

    def __init__(self, parent: tk.Misc, hotel: Hotel, número_habitación_reservada: int):
        super().__init__(parent)
        self.hotel = hotel
        self.número_habitación_reservada = número_habitación_reservada
        self.habitación_reservada: Habitación | None = None
        self.title("Ingreso")
        self.geometry("290x250")
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
        pad = {"padx": 3, "pady": 3}

        tk.Label(self, text=f"Habitación {self.número_habitación_reservada}").grid(
            row=0, column=0, sticky="w", **pad
        )

        tk.Label(self, text="Fecha (AAAA-MM-DD):").grid(row=1, column=0, sticky="w", **pad)
        self.campo_fecha_ingreso = tk.Entry(self)
        self.campo_fecha_ingreso.grid(row=1, column=1, sticky="ew", **pad)

        tk.Label(self, text="Huésped").grid(row=2, column=0, sticky="w", **pad)

        tk.Label(self, text="Nombre:").grid(row=3, column=0, sticky="w", **pad)
        self.campo_nombre = tk.Entry(self)
        self.campo_nombre.grid(row=3, column=1, sticky="ew", **pad)

        tk.Label(self, text="Apellidos:").grid(row=4, column=0, sticky="w", **pad)
        self.campo_apellidos = tk.Entry(self)
        self.campo_apellidos.grid(row=4, column=1, sticky="ew", **pad)

        tk.Label(self, text="Doc. Identidad:").grid(row=5, column=0, sticky="w", **pad)
        self.campo_documento_identidad = tk.Entry(self)
        self.campo_documento_identidad.grid(row=5, column=1, sticky="ew", **pad)

        tk.Button(self, text="Aceptar", command=self._aceptar).grid(
            row=6, column=0, sticky="ew", **pad
        )
        tk.Button(self, text="Cancelar", command=self._cancelar).grid(
            row=6, column=1, sticky="ew", **pad
        )

    def _aceptar(self) -> None:
        for i, habitación in enumerate(self.hotel.lista_habitaciones):
            if habitación.get_número_habitación() == self.número_habitación_reservada:
                fecha_str = self.campo_fecha_ingreso.get().strip()
                try:
                    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror(
                        "Mensaje", "La fecha no está en el formato solicitado", parent=self
                    )
                    return

                try:
                    nombres = self.campo_nombre.get().strip()
                    apellidos = self.campo_apellidos.get().strip()
                    doc_id = int(self.campo_documento_identidad.get().strip())
                    if not nombres or not apellidos:
                        raise ValueError("Campos de nombre o apellido vacíos")

                    huésped = Huésped(nombres, apellidos, doc_id)
                    huésped.set_fecha_ingreso(fecha)
                    habitación.set_huésped(huésped)
                    habitación.set_disponible(False)
                    self.habitación_reservada = habitación
                    self.hotel.lista_habitaciones[i] = habitación

                    messagebox.showinfo(
                        "Mensaje", "El huésped ha sido registrado", parent=self
                    )
                    self.destroy()
                except Exception:
                    messagebox.showerror(
                        "Error", "Campo nulo o error en formato de numero", parent=self
                    )
                return

    def _cancelar(self) -> None:
        self.destroy()


# Clase VentanaHabitaciones
class VentanaHabitaciones(tk.Toplevel):
    """
    Define una ventana que muestra las diez habitaciones del hotel y su
    disponibilidad.
    """

    def __init__(self, parent: tk.Misc, hotel: Hotel):
        super().__init__(parent)
        self.hotel = hotel
        self.title("Habitaciones")
        self.geometry("760x260")
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
        for idx, habitación in enumerate(self.hotel.lista_habitaciones):
            fila = idx // 5
            col = idx % 5
            x = 20 + col * 140
            y_label = 30 if fila == 0 else 120
            y_disp = 50 if fila == 0 else 140

            tk.Label(self, text=f"Habitación {habitación.get_número_habitación()}").place(
                x=x, y=y_label, width=130, height=23
            )
            estado = "Disponible" if habitación.get_disponible() else "No disponible"
            tk.Label(self, text=estado).place(x=x, y=y_disp, width=100, height=23)

        tk.Label(self, text="Habitación a reservar:").place(
            x=250, y=180, width=135, height=23
        )
        self.var_habitación = tk.IntVar(value=1)
        self.campo_habitación_seleccionada = tk.Spinbox(
            self, from_=1, to=10, textvariable=self.var_habitación
        )
        self.campo_habitación_seleccionada.place(x=380, y=180, width=50, height=23)

        tk.Button(self, text="Aceptar", command=self._aceptar).place(
            x=500, y=180, width=100, height=23
        )

    def _aceptar(self) -> None:
        try:
            número_hab = int(self.campo_habitación_seleccionada.get())
        except ValueError:
            messagebox.showerror("Error", "Número de habitación inválido", parent=self)
            return

        if not self.hotel.buscar_habitación_ocupada(número_hab):
            ventana_ingreso = VentanaIngreso(self.master, self.hotel, número_hab)
            self.withdraw()
            ventana_ingreso.focus_set()
        else:
            messagebox.showinfo("Mensaje", "La habitación está ocupada", parent=self)

# Clase VentanaPrincipal
class VentanaPrincipal(tk.Tk):
    """
    Define una interfaz gráfica que permitirá gestionar el ingreso y salida
    de huéspedes a un hotel.
    """

    def __init__(self, hotel: Hotel):
        super().__init__()
        self.hotel = hotel
        self.title("Hotel")
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
            label="Consultar habitaciones", command=self._consultar_habitaciones
        )
        menu_opciones.add_command(
            label="Salida de huéspedes", command=self._salida_huéspedes
        )
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

    def _consultar_habitaciones(self) -> None:
        VentanaHabitaciones(self, self.hotel)

    def _salida_huéspedes(self) -> None:
        # Nota: VentanaSalida no aparece en el extracto del libro, pero se deja el flujo listo
        messagebox.showinfo(
            "Salida de huéspedes",
            "Módulo de salida de huéspedes (VentanaSalida no incluida en el extracto).",
            parent=self,
        )


if __name__ == "__main__":
    mi_hotel = Hotel()
    app = VentanaPrincipal(mi_hotel)
    app.mainloop()