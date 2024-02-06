from web3 import Web3
# URL de Infura para la red de Ethereum (debes reemplazar
"TU-PROYECTO-ID" #con tu propio ID de proyecto de Infura)
ganache_url = "HTTP://127.0.0.1:7545"
# Crear una instancia de Web3 y conectarse a Infura
web3 = Web3(Web3.HTTPProvider(ganache_url))
# Verificar la conexión
if web3.is_connected():
    print("Conexión exitosa a Infura")
else:
    print("No se pudo conectar a Infura. Por favor, verifica la URL o tu conexión a Internet.")
    

#Send eth from one address to another
account1 = '0x14d9Cb08D9EC82248f80ce136321e9cbDc4A51a2'
account2 = '0x6d4BD9D9891Dc50aA525077760E214E0BeB13225'
account3 = '0x6F24AE3A708CC0EB4c2C5331F04642F31e78e60C'


contractAddress = '0x4e140a6E8F956B0215a752DB62d3b430855f2783'

#Compruebo si tiene formato válido la primera cuenta
if not web3.is_checksum_address(account1):
    print('Error: La primera cuenta no es válida')
    exit()
elif not web3.is_checksum_address(account2):
    print('Error: La segunda cuenta no es válida')
    exit()


private_key = '0xdef6cbd4f42085724924f5e812adc211ad86e749b7bd47716969b5f1cd0eb9c0'

nonce = web3.eth.get_transaction_count(account1)

#Comprobamos si las cuentas tienen fondos
balance_1 = web3.eth.get_balance(account1)
balance_2 = web3.eth.get_balance(account2)

if balance_1 == 0:
    print('Error: no hay fondos')
    exit()
elif balance_2 == 0:
    print('Error: la cuenta 2 no tiene fondos')
    exit()
else:
    print('Ambas cuentas existen')



tx = {
    'nonce': nonce,
    'to': account2,
    'value':web3.to_wei(1, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.to_wei('50','gwei')
}

try:
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print('Tx realizada \nNumero de la transaccion', web3.to_hex(tx_hash))
except ValueError:
    print('Error: firma no válida')