
from cryptography.fernet import Fernet


key = 'Jaa6Pe1aQqF6X2-b0jmuVFUulYZ-B8kXE9T_YcBKEY4='

objeto_cifrado = Fernet(key)

def Encriptar(text):

    texto_encriptado = objeto_cifrado.encrypt(str.encode(text))
    
    return texto_encriptado

def Desencriptar(text):
    text = text.encode()
    texto_desencriptado_bytes = objeto_cifrado.decrypt(text)
    texto_desencriptado = texto_desencriptado_bytes.decode()
    return texto_desencriptado

#print(Encriptar("Rxd.Rp"))