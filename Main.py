from PrestamoDeFi import altaPrestamista

def menu():
    print("Bienvenido al menú de opciones:")
    print("1. Alta de prestamista")
    print("2. Opción 2")
    print("3. Opción 3")
    print("4. Salir")

def altaPrestamista():
    print("Has seleccionado la opción de alta de prestamista.")
    # Aquí iría la lógica para el alta de prestamista

def opcion_2():
    print("Has seleccionado la opción 2.")
    # Aquí iría la lógica para la opción 2

def opcion_3():
    print("Has seleccionado la opción 3.")
    # Aquí iría la lógica para la opción 3

def main():
    while True:
        menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            altaPrestamista()
        elif opcion == "2":
            opcion_2()
        elif opcion == "3":
            opcion_3()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

if __name__ == "__main__":
    main()