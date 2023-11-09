import json

class Usuario:
    def __init__(self, nombre, apellido, edad, tipo):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.tipo = tipo  # VIP o estándar
        self.reservas = []

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo}) - Edad: {self.edad}"

    def crear_reserva(self, concierto, cantidad_boletos):
        reserva = {"concierto": concierto, "cantidad_boletos": cantidad_boletos}
        self.reservas.append(reserva)
        print(f"Reserva creada para el concierto {concierto} - {cantidad_boletos} boletos")

    def generar_factura(self):
        factura = {"usuario": str(self), "reservas": self.reservas}
        with open(f"{self.nombre}_{self.apellido}_factura.json", "w") as file:
            json.dump(factura, file)
        print("Factura generada y almacenada.")

class Bar:
    def __init__(self):
        self.bebidas = {
            "alcoholicas": [
                {"nombre": "Cerveza", "precio": 5.0},
                {"nombre": "Vino tinto", "precio": 10.0},
                {"nombre": "Ron", "precio": 8.0},
                {"nombre": "Whisky", "precio": 12.0},
                {"nombre": "Gin Tónico", "precio": 7.0}
            ],
            "no_alcoholicas": [
                {"nombre": "Agua", "precio": 1.0},
                {"nombre": "Refresco de cola", "precio": 3.0},
                {"nombre": "Jugo de naranja", "precio": 2.0},
                {"nombre": "Limonada", "precio": 2.5},
                {"nombre": "Té helado", "precio": 2.0}
            ]
        }
        self.boletos_vip_disponibles = 40
        self.palco_disponible = True

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

def main():
    usuarios = []
    concierto = "Inquietos del Vallenato"
    sistema_abierto = True

    while sistema_abierto:
        print("1. Crear perfil de usuario")
        print("2. Acceder al sistema")
        print("3. Salir del sistema")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            tipo = input("Tipo de usuario (VIP o estándar): ").upper()
            if edad < 18:
                print("Lo siento, debes ser mayor de edad para registrarte.")
                continue
            usuario = Usuario(nombre, apellido, edad, tipo)
            usuarios.append(usuario)
            print("Perfil de usuario creado.")

        elif opcion == "2":
            if not usuarios:
                print("No hay usuarios registrados. Por favor, crea un perfil primero.")
                continue
            nombre = input("Nombre de usuario: ")
            apellido = input("Apellido de usuario: ")
            usuario = None
            for u in usuarios:
                if u.nombre == nombre and u.apellido == apellido:
                    usuario = u
                    break

            if usuario:
                print(f"Bienvenido, {str(usuario)}")
                if usuario.edad < 18:
                    print("Lo siento, debes ser mayor de edad para acceder al sistema.")
                    continue
                bar = Bar()
                bar.mostrar_bebidas(usuario.tipo)
                bebida = input("Selecciona una bebida: ")
                cantidad = int(input("Cantidad: "))
                if bebida == "VIP":
                    if usuario.tipo != "VIP":
                        print("Lo siento, solo los usuarios VIP pueden seleccionar boletos VIP.")
                        continue
                    if bar.boletos_vip_disponibles > 0:
                        usuario.crear_reserva(concierto, cantidad)
                        bar.boletos_vip_disponibles -= cantidad
                        print(f"Boletos VIP reservados - Boletos VIP disponibles: {bar.boletos_vip_disponibles}")
                    else:
                        print("Lo siento, no quedan boletos VIP disponibles.")
                elif bebida == "Palco":
                    if not bar.palco_disponible:
                        print("Lo siento, el palco ya está ocupado.")
                        continue
                    usuario.crear_reserva(concierto, cantidad)
                    bar.palco_disponible = False
                    print("Palco reservado.")
                else:
                    bar.seleccionar_bebida(usuario.tipo, bebida, cantidad)
                    usuario.crear_reserva(concierto, cantidad)
                usuario.generar_factura()
            else:
                print("Usuario no encontrado. Asegúrate de crear un perfil primero.")

        elif opcion == "3":
            sistema_abierto = False

if __name__ == "__main__":
    main()