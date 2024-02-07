
from functions import alta_prestamista
from env import *
from web3 import Web3

web3 = Web3(Web3.HTTPProvider(ganache_url))

prestamistas = []
clientes = []

def menu():
    print("Bienvenido al menú de opciones:")
    print("1. Alta de prestamista")
    print("2. Opción 2")
    print("3. Opción 3")
    print("4. Salir")



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
            nuevo_prestamista = input('Introduce el address del nuevo prestamista: ')
            #Check if the input address is correct
            if not web3.is_checksum_address(nuevo_prestamista):
                print('Error: La primera cuenta no es válida')
                exit()
            alta_prestamista(nuevo_prestamista, abi_contrato)
            prestamistas.append(nuevo_prestamista)
            #PRUEBA: se ejecuta dos veces para ver el mensaje "YA estás dado de alta"
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