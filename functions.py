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
        
def registrar_nuevo_cliente(nuevo_cliente_address, prestamista_address, abi_contrato):
   
    # Conexión a la red Ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    abiContrato = json.loads(abi_contrato)

    instancia_sc = web3.eth.contract(address = contractAddress, abi=abiContrato)


    # Crear la transacción para registrar al nuevo cliente
    transaccion = contrato.functions.registrarCliente(nuevo_cliente_address).buildTransaction({
        'chainId': 1,  # Identificador de la red Ethereum
        'gas': 2000000,  # Limite de gas
        'gasPrice': web3.toWei('50', 'gwei'),  # Precio del gas
        'nonce': web3.eth.getTransactionCount(prestamista_address)  # Contador de transacciones
    })

    # Firmar la transacción con la clave privada del prestamista
    transaccion_firmada = web3.eth.account.signTransaction(transaccion, private_key=prestamista_private_key)

    # Enviar la transacción
    tx_hash = web3.eth.sendRawTransaction(transaccion_firmada.rawTransaction)

    # Esperar la confirmación de la transacción
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Retornar el resultado
    print("El cliente ha sido registrado con éxito.")