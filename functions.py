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
    
    # Primero, depositar la garantía utilizando la función del contrato
     tx_hash = instancia_sc.functions.depositarGarantia().transact({'from': cliente_address})
     receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Segundo, enviar el monto de ether al contrato como garantía
     nonce = web3.eth.get_transaction_count(cliente_address)
     tx = {
        'nonce': nonce,
        'to': contractAddress,
        'value': web3.to_wei(monto, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    }

     try:
         signed_tx = web3.eth.account.sign_transaction(tx, cliente_private_key)
         tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
         print('Transacción de garantía realizada.\nNúmero de transacción:', web3.to_hex(tx_hash))
     except ValueError:
        print('Error: firma no válida')
        
        
def solicitar_prestamo(cliente_address, abi_contrato, monto, plazo):
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    abiContrato = json.loads(abi_contrato)
    instancia_sc = web3.eth.contract(address=contractAddress, abi=abiContrato)

    # Obtener el saldo de garantía del cliente
    saldo_garantia = instancia_sc.functions.clientes(cliente_address).call()[1]

    # Verificar si el cliente tiene suficiente saldo de garantía
    if saldo_garantia < monto:
        print("Error: No tienes suficiente saldo de garantía para solicitar este préstamo")
        return None

    # Crear la transacción para solicitar el préstamo
    tx_hash = instancia_sc.functions.solicitarPrestamos(monto, plazo).transact({'from': cliente_address})

    # Esperar la confirmación de la transacción y obtener el ID del nuevo préstamo
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    nuevo_id_prestamo = receipt['events']['SolicitudPrestamo']['returnValues']['0']

    print("Solicitud de préstamo realizada con éxito. ID del nuevo préstamo:", nuevo_id_prestamo)
    return nuevo_id_prestamo