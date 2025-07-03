from cryptography.fernet import Fernet

FERNET_KEY = Fernet.generate_key()  # You can save/load this from env
fernet = Fernet(FERNET_KEY)

def encrypt_id(file_id: int) -> str:
    return fernet.encrypt(str(file_id).encode()).decode()

def decrypt_id(token: str) -> int:
    return int(fernet.decrypt(token.encode()).decode())
