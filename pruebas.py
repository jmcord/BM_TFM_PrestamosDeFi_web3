from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from eth_account import Account
from env import *
    
id_prestamo = 4
cliente_address = '0xb932637De09280c9f30f2Edd03a9a23E35408913'   
prestamista_address = '0x6d4BD9D9891Dc50aA525077760E214E0BeB13225'
cliente_private_key = '0x4fe9230b4cac7edad7472e466e1a254d5f66a30e295e44833f19df20bb04ebc3'    
contractAddress = '0xfb7D7f64Fce552320cCC7631841f05A99B82628C'
prestamista_private_key = '0x3eea2e615ec68a4ca2c595bd8d184fc424518015a154cc4cc2ce25001a34abed' 
socio_principal = '0x14d9Cb08D9EC82248f80ce136321e9cbDc4A51a2'
socio_private_key = '0xdef6cbd4f42085724924f5e812adc211ad86e749b7bd47716969b5f1cd0eb9c0'   
# Conexión a la red Ganache
ganache_url = "HTTP://127.0.0.1:7545"
# Crear una instancia de Web3 y conectarse a Infura
web3 = Web3(Web3.HTTPProvider(ganache_url))
# Verificar la conexión
if web3.is_connected():
    print("Conexión exitosa a Ganache")
else:
    print("No se pudo conectar a Ganache. Por favor, verifica la URL o tu conexión a Internet.")
abi_contrato = json.loads(abi_contrato)
instancia_sc = web3.eth.contract(address=contractAddress, abi=abi_contrato)
    # Obtener los detalles del préstamo
prestamo = instancia_sc.functions.obtenerDetalleDePrestamo(cliente_address, id_prestamo).call({'from': prestamista_address})
    
    #Obtener el monto
monto = int(prestamo[2])*10**18
    # Obtener el nonce
nonce = web3.eth.get_transaction_count(cliente_address)
    
    # Construir la transacción
tx = {
    'nonce': web3.eth.get_transaction_count(cliente_address),
    'to': socio_principal,
    'data': instancia_sc.encodeABI(fn_name='reembolsarPrestamo', args=[id_prestamo]),
    'gas': 2000000,
    'gasPrice': web3.to_wei('50', 'gwei'),
    'value': monto,
    'from': cliente_address #Ya que está en el modificador
    }
    
    # Firmar la transacción
signed_tx = web3.eth.account.sign_transaction(tx, cliente_private_key)

    # Enviar la transacción firmada
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # Esperar la confirmación de la transacción
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
print("Transacción confirmada. Préstamo reembolsado con éxito.")   