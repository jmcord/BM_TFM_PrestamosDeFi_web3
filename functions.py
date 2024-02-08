from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from eth_account import Account
from env import *



def alta_prestamista(nuevo_prestamista, abi_contrato):
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abiContrato = json.loads(abi_contrato)

    instancia_sc = web3.eth.contract(address = contractAddress, abi=abiContrato)
    
    # Llamar a la función solo si el propietario está llamando
    if socio_principal == '0x14d9Cb08D9EC82248f80ce136321e9cbDc4A51a2':  
        tx_hash = instancia_sc.functions.altaPrestamista(nuevo_prestamista).transact({'from': socio_principal})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Transacción confirmada. Empleado prestamista dado de alta.")
    else:
        print('No tienes permiso para llamar a esta función')
        
def alta_cliente(nuevo_cliente_address, prestamista_address, abi_contrato):
   
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    abiContrato = json.loads(abi_contrato)

    instancia_sc = web3.eth.contract(address = contractAddress, abi=abiContrato)


    # Crear la transacción para registrar al nuevo cliente
    tx_hash = instancia_sc.functions.altaCliente(nuevo_cliente_address).transact({'from': prestamista_address})
    web3.eth.wait_for_transaction_receipt(tx_hash)
 

    # Retornar el resultado
    print("El cliente ha sido registrado con éxito.")
    
    

def depositar_garantia(cliente_address, abi_contrato, monto):
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abiContrato = json.loads(abi_contrato)
    instancia_sc = web3.eth.contract(address=contractAddress, abi=abiContrato)
    
    # Convertir el monto a wei
    monto_wei = web3.to_wei(monto, 'ether')
    

    # Luego, depositamos la garantía utilizando la función del contrato
    tx_hash = instancia_sc.functions.depositarGarantia().transact({'from': cliente_address, 'value': monto_wei})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print("Transacción confirmada. Garantía depositada con éxito.")
    return receipt

        
def solicitar_prestamo(cliente_address, abi_contrato, monto, plazo):
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abiContrato = json.loads(abi_contrato)
    instancia_sc = web3.eth.contract(address=contractAddress, abi=abiContrato)

    # Obtener el saldo de garantía del cliente
    saldo_garantia = instancia_sc.functions.clientes(cliente_address).call()[1]

    # Convertir el monto a wei
    monto_wei = web3.to_wei(monto, 'ether')

    # Verificar si el cliente tiene suficiente saldo de garantía
    if saldo_garantia < monto_wei:
        print("Error: No tienes suficiente saldo de garantía para solicitar este préstamo")
        return None

    # Crear la transacción para solicitar el préstamo
    tx_hash = instancia_sc.functions.solicitarPrestamos(monto_wei, plazo).transact({'from': cliente_address})

    # Esperar la confirmación de la transacción y obtener el ID del nuevo préstamo
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)


    print("Solicitud de préstamo realizada con éxito")

def obtener_detalle_de_prestamo(cliente_address, id_, abi_contrato):
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abi_contrato = json.loads(abi_contrato)
    instancia_sc = web3.eth.contract(address=contractAddress, abi=abi_contrato)
    
    # Llama a la función obtenerDetalleDePrestamo del contrato
    detalle_prestamo = instancia_sc.functions.obtenerDetalleDePrestamo(cliente_address, id_).call()
    
    # La variable 'detalle_prestamo' ahora contiene la información del préstamo
    print("Detalle del préstamo:", detalle_prestamo)
    return detalle_prestamo


def aprobar_prestamo(prestatario_address, abi_contrato, id_prestamo, prestamista_address):
    #MEJORA: modificar el struct de Prestamo para que incluya el prestamista, y acceder por prestamo[i] en lugar de por parámetro
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abi_contrato = json.loads(abi_contrato)
    instancia_sc = web3.eth.contract(address=contractAddress, abi=abi_contrato)
    
    # Verificar si el empleado prestamista está llamando a la función
    empleado_prestamista = prestatario_address #MEJORA: acceder al mapping y ver si está ahí
    if empleado_prestamista != prestatario_address:
        print("Error: No tienes permiso para llamar a esta función.")
        return
    
    # Obtener los detalles del préstamo
    prestamo = instancia_sc.functions.obtenerDetalleDePrestamo(prestatario_address, id_prestamo).call({'from': prestamista_address})
    #MEJORA: llamar a la lista de ids y ver si está ahí y comprobar:
    #if id_prestamo not in prestamos_ids:
    #    print("Error: Préstamo no asignado al prestatario.")
    #    return
    
    
    if prestamo[6]:
        print("Error: Préstamo ya aprobado.")
        return
    if prestamo[7]:
        print("Error: Préstamo ya reembolsado.")
        return
    if prestamo[8]:
        print("Error: Préstamo ya liquidado.")
        return
    
    # Aprobar el préstamo
    tx_hash = instancia_sc.functions.aprobarPrestamo(prestatario_address, id_prestamo).transact({'from': prestamista_address})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print("Transacción confirmada. Préstamo aprobado.")
    return receipt


def reembolsar_prestamo2(id_prestamo, cliente_address, abi_contrato):
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abi_contrato = json.loads(abi_contrato)
    instancia_sc = web3.eth.contract(address=contractAddress, abi=abi_contrato)
    
    # Llama a la función reembolsarPrestamo del contrato
    tx_hash = instancia_sc.functions.reembolsarPrestamo(id_prestamo).transact({'from': cliente_address})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print("Transacción confirmada. Préstamo reembolsado con éxito.")
    return receipt


def reembolsar_prestamo(id_prestamo, prestatario_address cliente_address, abi_contrato, cliente_private_key):
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abi_contrato = json.loads(abi_contrato)
    instancia_sc = web3.eth.contract(address=contractAddress, abi=abi_contrato)
    # Obtener los detalles del préstamo
    prestamo = instancia_sc.functions.obtenerDetalleDePrestamo(prestatario_address, id_prestamo).call({'from': prestamista_address})
    # Obtener el nonce
    nonce = web3.eth.get_transaction_count(cliente_address)
    
    # Construir la transacción
    tx = {
        'nonce': nonce,
        'to': contractAddress,
        'data': instancia_sc.encodeABI(fn_name='reembolsarPrestamo', args=[id_prestamo]),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'value': 0
    }
    
    # Firmar la transacción
    signed_tx = web3.eth.account.sign_transaction(tx, cliente_private_key)
    
    # Enviar la transacción firmada
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # Esperar la confirmación de la transacción
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print("Transacción confirmada. Préstamo reembolsado con éxito.")
    return receipt