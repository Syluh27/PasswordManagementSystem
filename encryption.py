from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64

# Clave maestra para cifrar y descifrar
PASSWORD_KEY = b"mi_clave_segura"
SALT = b"random_salt_value"


# Función para derivar la clave AES desde la contraseña maestra
def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password)


KEY = derive_key(PASSWORD_KEY, SALT)  # Generamos la clave AES


# Función para cifrar datos
def encrypt_password(password: str) -> tuple:
    iv = os.urandom(12)  # Generar IV aleatorio
    cipher = Cipher(algorithms.AES(KEY), modes.GCM(iv))
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()
    return base64.b64encode(iv).decode(), base64.b64encode(encrypted_password).decode(), base64.b64encode(
        encryptor.tag).decode()


# Función para descifrar datos
def decrypt_password(encrypted_password: str, iv: str, tag: str) -> str:
    iv = base64.b64decode(iv)
    encrypted_password = base64.b64decode(encrypted_password)
    tag = base64.b64decode(tag)
    cipher = Cipher(algorithms.AES(KEY), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    return (decryptor.update(encrypted_password) + decryptor.finalize()).decode()


if __name__ == "__main__":
    # Prueba de cifrado y descifrado
    test_password = "MiContraseñaSegura123!"
    iv, encrypted, tag = encrypt_password(test_password)
    decrypted = decrypt_password(encrypted, iv, tag)

    print("Original:", test_password)
    print("Cifrado:", encrypted)
    print("Descifrado:", decrypted)
