
from functions import alta_prestamista, alta_cliente, depositar_garantia, solicitar_prestamo, aprobar_prestamo, reembolsar_prestamo, obtener_detalle_de_prestamo, obtener_prestamos_por_prestatario, liquidar_garantia
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
    print("5. aprobar prestamo")
    print("6. reembolsar prestamo")
    print("7. liquidar garantía")
    print("8. Obtener préstamos por prestatario")
    print("9. Obtener detalle prestamo")    
    print("0. Salir")



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
            #PRUEBAS: 1-solicitar más ETH que los depositados en garantía
        elif opcion == "5":
            prestamo_id = int(input('Introduce el id del prestamo: '))
            prestamista_address = input('Introduce el address del prestamista: ')
            prestatario_address = input('Introduce el address del cliente: ')
            #Check if the input address is correct
            #PRUEBA: verificamos addresses
            if not web3.is_checksum_address(prestamista_address):
                print('Error: La cuenta prestamista no es válida')
                exit()

            aprobar_prestamo(prestatario_address, abi_contrato, prestamo_id, prestamista_address)
            #PRUEBAS: 1-solicitar dos veces el mismo id
            #PRUEBAS: 2-utilizar un id incorrecto
            #PRUEBAS: 3-utilizar un prestamista no dado de alta
        elif opcion == "6":
            prestamo_id = int(input('Introduce el id del prestamo: '))
            prestatario_address = input('Introduce el address del cliente: ')
            prestamista_address = input('Introduce el address del prestamista: ')
            #Check if the input address is correct
            #PRUEBA: verificamos addresses
            if not web3.is_checksum_address(prestatario_address):
                print('Error: La cuenta prestatario no es válida')
                exit()

            reembolsar_prestamo(prestamo_id, prestamista_address, prestatario_address, abi_contrato, cliente_private_key)
            #PRUEBAS: 1-reembolsar dos veces el mismo id
            #PRUEBAS: 2-utilizar un id incorrecto
            
        elif opcion == "7":
            prestamo_id = int(input('Introduce el id del prestamo: '))
            prestatario_address = input('Introduce el address del cliente: ')
            #Check if the input address is correct
            #PRUEBA: verificamos addresses
            if not web3.is_checksum_address(prestatario_address):
                print('Error: La cuenta prestatario no es válida')
                exit()

            liquidar_garantia(prestamo_id, prestatario_address, abi_contrato, cliente_private_key)
            #PRUEBAS: 1-reembolsar dos veces el mismo id
            #PRUEBAS: 2-utilizar un id incorrecto
            
        elif opcion == "8":
            prestatario_address = input('Introduce el address del cliente: ')
            #Check if the input address is correct
            #PRUEBA: verificamos addresses
            if not web3.is_checksum_address(prestatario_address):
                print('Error: La cuenta prestatario no es válida')
                exit()

            prestamos = obtener_prestamos_por_prestatario(prestatario_address, abi_contrato)
            print(prestamos)
            #PRUEBAS: 1-introducir un address inexistente
      

            
        elif opcion == "9":
            prestamo_id = int(input('Introduce el id del prestamo: '))
            prestatario_address = input('Introduce el address del cliente: ')
            #Check if the input address is correct
            #PRUEBA: verificamos addresses
            if not web3.is_checksum_address(prestatario_address):
                print('Error: La cuenta prestatario no es válida')
                exit()

            prestamo = obtener_detalle_de_prestamo(prestatario_address, prestamo_id, abi_contrato)
            print(prestamo)
            #PRUEBAS: 1-introducir un id inexistente
            #PRUEBAS: 2-introducir un address inexistente

    
      
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")


if __name__ == "__main__":
    main()