
from functions import alta_prestamista, alta_cliente, depositar_garantia, solicitar_prestamo
from env import *
from web3 import Web3

web3 = Web3(Web3.HTTPProvider(ganache_url))

prestamistas = []
clientes = []

def menu():
    print("Bienvenido al menú de opciones:")
    print("1. Alta de prestamista")
    print("2. Alta de cliente")
    print("3. Depositar Garantia")
    print("4. solicitar prestamo")
    print("10. Salir")



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
            nuevo_cliente = input('Introduce el address del nuevo cliente: ')
            prestamista_address = input('Introduce el address del prestamista: ')
            #Check if the input address is correct
            #PRUEBA: verificamos addresses
            if not web3.is_checksum_address(nuevo_cliente):
                print('Error: La cuenta cliente no es válida')
                exit()
            if not web3.is_checksum_address(prestamista_address):
                print('Error: La cuenta prestamista no es válida')
                exit()
            alta_cliente(nuevo_cliente, prestamista_address, abi_contrato)
            clientes.append(nuevo_cliente)
            #PRUEBA: 1-se ejecuta dos veces para ver el mensaje "YA estás dado de alta"
            #PRUEBA: 2-se ejecuta introduciendo un address que no pertenece al prestamista"
        elif opcion == "3":
            monto = int(input('Introduce la garantia: '))
            cliente_address = input('Introduce el address del cliente: ')
            #Check if the input address is correct
            #PRUEBA: verificamos addresses
            if not web3.is_checksum_address(cliente_address):
                print('Error: La cuenta cliente no es válida')
                exit()

            depositar_garantia(cliente_address, abi_contrato, monto)
            if cliente_address not in clientes:
                clientes.append(cliente_address)
            #PRUEBA: 1-tratar de depositar una cantidad mayor a 100 ETH
        elif opcion == "4":
            monto = int(input('Introduce el monto del prestamo: '))
            cliente_address = input('Introduce el address del cliente: ')
            plazo = int(input('Introduce el plazo en segundos: '))
            #Check if the input address is correct
            #PRUEBA: verificamos addresses
            if not web3.is_checksum_address(cliente_address):
                print('Error: La cuenta cliente no es válida')
                exit()

            solicitar_prestamo(cliente_address, abi_contrato, monto, plazo)

        elif opcion == "10":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")


if __name__ == "__main__":
    main()