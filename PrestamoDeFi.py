from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from eth_account import Account
# URL de Infura para la red de Ethereum (debes reemplazar
"TU-PROYECTO-ID" #con tu propio ID de proyecto de Infura)
ganache_url = "HTTP://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(ganache_url))
# Verificar la conexión
if web3.is_connected():
    print("Conexión exitosa a Ganache")
else:
    print("No se pudo conectar a Ganache. Por favor, verifica la URL o tu conexión a Internet.")
    

#Send eth from one address to another
account1 = '0x14d9Cb08D9EC82248f80ce136321e9cbDc4A51a2'
account2 = '0x6d4BD9D9891Dc50aA525077760E214E0BeB13225'
account3 = '0x6F24AE3A708CC0EB4c2C5331F04642F31e78e60C'


contractAddress = '0x4e140a6E8F956B0215a752DB62d3b430855f2783'
abi_contrato = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"GarantiaLiquidada","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoAprobado","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoReembolsado","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"plazo","type":"uint256"}],"name":"SolicitudPrestamo","type":"event"},{"inputs":[{"internalType":"address","name":"_nuevoCliente","type":"address"}],"name":"altaCliente","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_nuevoPrestamista","type":"address"}],"name":"altaPrestamista","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"aprobarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"clientes","outputs":[{"internalType":"bool","name":"activado","type":"bool"},{"internalType":"uint256","name":"saldoGarantia","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"depositarGarantia","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"empleadosPrestamista","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"liquidarGarantia","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"obtenerDetalleDePrestamo","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"prestatario","type":"address"},{"internalType":"uint256","name":"monto","type":"uint256"},{"internalType":"uint256","name":"plazo","type":"uint256"},{"internalType":"uint256","name":"tiempoSolicitud","type":"uint256"},{"internalType":"uint256","name":"tiempoLimite","type":"uint256"},{"internalType":"bool","name":"aprobado","type":"bool"},{"internalType":"bool","name":"reembolsado","type":"bool"},{"internalType":"bool","name":"liquidado","type":"bool"}],"internalType":"struct PrestamoDeFi.Prestamo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"}],"name":"obtenerPrestamosPorPrestatario","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"reembolsarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"socioPrincipal","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"monto_","type":"uint256"},{"internalType":"uint256","name":"plazo_","type":"uint256"}],"name":"solicitarPrestamos","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]')


owner_account = '0x14d9Cb08D9EC82248f80ce136321e9cbDc4A51a2'
#Compruebo si tiene formato válido la primera cuenta
if not web3.is_checksum_address(account1):
    print('Error: La primera cuenta no es válida')
    exit()
elif not web3.is_checksum_address(account2):
    print('Error: La segunda cuenta no es válida')
    exit()




# Crear instancia SC
instancia_sc = web3.eth.contract(address = contractAddress, abi=abi_contrato)
# Dirección del nuevo prestamista
nuevo_prestamista = "0x6d4BD9D9891Dc50aA525077760E214E0BeB13225"  # Reemplaza con la dirección del nuevo prestamista

# Obtener la dirección del socio principal
socio_principal = instancia_sc.functions.socioPrincipal().call()
print(f'el socio es : {socio_principal}')
print("Dirección del socio principal:", socio_principal)


# Llamar a la función solo si el propietario está llamando
if owner_account == socio_principal:  # Reemplazar 'OWNER_ADDRESS' por la dirección del propietario
    tx_hash = instancia_sc.functions.altaPrestamista(nuevo_prestamista).transact({'from': owner_account})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transacción confirmada. Empleado prestamista dado de alta.")
else:
    print('No tienes permiso para llamar a esta función')
    
    
    
    
    
    