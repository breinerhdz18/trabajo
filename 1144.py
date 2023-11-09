import tkinter as tk
from tkinter import messagebox
import json
usuarios = []
concierto = "Los inquietos del vallenato"
root = tk.Tk()
root.title("Los inquietos del vallenato") 
#REQUISITO DE  crear usuario"
class Usuario:
    def __init__(self, nombre, apellido, edad, tipo):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.tipo = tipo  # VIP o estándar
        self.reservas = []

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo}) - Edad: {self.edad}"
#Crear reserva#
    def crear_reserva(self, concierto, cantidad_boletos):
        reserva = {"concierto": concierto, "cantidad_boletos": cantidad_boletos}
        self.reservas.append(reserva)
        print(f"Reserva creada para el concierto {concierto} - {cantidad_boletos} boletos")
#Generar factura#
    def generar_factura(self):
        factura = {"usuario": str(self), "reservas": self.reservas}
        with open(f"{self.nombre}_{self.apellido}_factura.json", "w") as file:
            json.dump(factura, file)
        print("Factura generada y almacenada.")
#Crear bar#
class Bar:
    def __init__(self):
        self.bebidas = {
            "alcoholicas": [
                {"nombre": "Cerveza", "precio": 5.000},
                {"nombre": "Vino tinto", "precio": 10.000},
                {"nombre": "Ron", "precio": 80.000},
                {"nombre": "Whisky", "precio": 120.000},
                {"nombre": "Gin Tónico", "precio": 70.000}
            ],
            "no_alcoholicas": [
                {"nombre": "Agua", "precio": 1.000},
                {"nombre": "Refresco de cola", "precio": 3.000},
                {"nombre": "Jugo de naranja", "precio": 2.000},
                {"nombre": "Limonada", "precio": 2.500},
                {"nombre": "Té helado", "precio": 2.000}
            ]
        }
        self.boletos_vip_disponibles = 40
        self.palco_disponible = True
#Mostrar bebidas
    def mostrar_bebidas(self, tipo_usuario):
        print("Bebidas disponibles:")
        for categoria in self.bebidas:
            print(f"{categoria.capitalize()}:")
            for bebida in self.bebidas[categoria]:
                precio = bebida["precio"]
                if tipo_usuario == "VIP":
                    precio *= 0.75
                print(f"{bebida['nombre']} - ${precio:.2f}")

    def seleccionar_bebida(self, tipo_usuario, bebida, cantidad):
        for categoria in self.bebidas:
            for b in self.bebidas[categoria]:
                if bebida == b["nombre"]:
                    precio = b["precio"]
                    if tipo_usuario == "VIP":
                        precio *= 0.75
                    total = precio * cantidad
                    print(f"{cantidad} {bebida} seleccionada(s) - Total: ${total:.2f}")
                    return
        print(f"{bebida} no está en el menú")
        #INTERFAZ DE REQUISITOS"
#Crear Perfil(parte de interfaz) #
def crear_perfil():
    perfil_window = tk.Toplevel(root)
    perfil_window.title("Crear Perfil")

    label_nombre = tk.Label(perfil_window, text="Nombre:")
    label_nombre.grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(perfil_window)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    label_apellido = tk.Label(perfil_window, text="Apellido:")
    label_apellido.grid(row=1, column=0, padx=10, pady=5)
    entry_apellido = tk.Entry(perfil_window)
    entry_apellido.grid(row=1, column=1, padx=10, pady=5)

    label_edad = tk.Label(perfil_window, text="Edad:")
    label_edad.grid(row=2, column=0, padx=10, pady=5)
    entry_edad = tk.Entry(perfil_window)
    entry_edad.grid(row=2, column=1, padx=10, pady=5)

    label_tipo = tk.Label(perfil_window, text="Tipo de usuario (VIP o estándar):")
    label_tipo.grid(row=3, column=0, padx=10, pady=5)
    entry_tipo = tk.Entry(perfil_window)
    entry_tipo.grid(row=3, column=1, padx=10, pady=5)
#Guardar perfil#
    def guardar_perfil():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        edad = int(entry_edad.get())
        tipo = entry_tipo.get().upper()

        if edad < 18:
            messagebox.showerror("Error", "Debes ser mayor de edad para registrarte.")
            return

        usuario = Usuario(nombre, apellido, edad, tipo)
        usuarios.append(usuario)
        messagebox.showinfo("Perfil Creado", "Perfil de usuario creado con éxito.")
        perfil_window.destroy()

    boton_guardar = tk.Button(perfil_window, text="Guardar Perfil", command=guardar_perfil)
    boton_guardar.grid(row=4, columnspan=2, pady=10)
    #interfaz#
def acceder_sistema():
    acceso_window = tk.Toplevel(root)
    acceso_window.title("Acceder al Sistema")

    label_nombre = tk.Label(acceso_window, text="Nombre de usuario:")
    label_nombre.grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(acceso_window)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    label_apellido = tk.Label(acceso_window, text="Apellido de usuario:")
    label_apellido.grid(row=1, column=0, padx=10, pady=5)
    entry_apellido = tk.Entry(acceso_window)
    entry_apellido.grid(row=1, column=1, padx=10, pady=5)
#Acceder Usuario"
    def acceder_usuario():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        usuario = None

        for u in usuarios:
            if u.nombre == nombre and u.apellido == apellido:
                usuario = u
                break

        if usuario:
            if usuario.edad < 18:
                messagebox.showerror("Error", "Debes ser mayor de edad para acceder al sistema.")
            else:
                acceder_sistema_real(usuario)
                acceso_window.destroy()
        else:
            messagebox.showerror("Error", "Usuario no encontrado. Asegúrate de crear un perfil primero.")

    boton_acceder = tk.Button(acceso_window, text="Acceder", command=acceder_usuario)
    boton_acceder.grid(row=2, columnspan=2, pady=10)
#Parte de la interfaz#
def acceder_sistema_real(usuario):
    bar = Bar()
    bar.mostrar_bebidas(usuario.tipo)
    bebida = input("Selecciona una bebida: ")
    cantidad = int(input("Cantidad: "))
    if bebida == "VIP":
        if usuario.tipo != "VIP":
            print("Lo siento, solo los usuarios VIP pueden seleccionar boletos VIP.")
            return
        if bar.boletos_vip_disponibles > 0:
            usuario.crear_reserva(concierto, cantidad)
            bar.boletos_vip_disponibles -= cantidad
            print(f"Boletos VIP reservados - Boletos VIP disponibles: {bar.boletos_vip_disponibles}")
        else:
            print("Lo siento, no quedan boletos VIP disponibles.")
    elif bebida == "Palco":
        if not bar.palco_disponible:
            print("Lo siento, el palco ya está ocupado.")
            return
        usuarios.crear_reserva(concierto, cantidad)
        bar.palco_disponible = False
        print("Palco reservado.")
    else:
        bar.seleccionar_bebida(usuario.tipo, bebida, cantidad)
        usuario.crear_reserva(concierto, cantidad)
    usuario.generar_factura()
def opcion_crear_perfil():
    crear_perfil()

def opcion_acceder_sistema():
    if not usuarios:
        messagebox.showerror("Error", "No hay usuarios registrados. Por favor, crea un perfil primero.")
    else:
        acceder_sistema()
def salir_sistema():
    root.quit()
def opcion_salir_sistema():
    salir_sistema()
etiqueta = tk.Label(root, text="Bienvenido al Sistema de Reservas")
etiqueta.pack(pady=20)
boton_crear_perfil = tk.Button(root, text="Crear Perfil", command=opcion_crear_perfil)
boton_crear_perfil.pack()
boton_acceder_sistema = tk.Button(root, text="Acceder al Sistema", command=opcion_acceder_sistema)
boton_acceder_sistema.pack()
boton_salir_sistema = tk.Button(root, text="Salir", command=opcion_salir_sistema)
boton_salir_sistema.pack(pady=20)
#ejecucion principal#
root.mainloop()