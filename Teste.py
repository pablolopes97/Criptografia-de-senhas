import hashlib
import base64
import json
from pathlib import Path
from cryptography.fernet import Fernet

class FernetHasher:
    base_dir = Path(__file__).resolve().parent
    key_dir = base_dir / "key"
    
    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()
        self.fernet = Fernet(key)

    @classmethod
    def create_key(cls, password):
        # Gera um hash da senha fornecida pelo usuário
        hasher = hashlib.sha256(password.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(hasher)

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.decrypt(value).decode()

def main():
    key_dir = Path("key")
    key_dir.mkdir(exist_ok=True)  # Cria o diretório se não existir
    data_file = key_dir / "passwords.json"

    # Usuário escolhe a senha de criptografia
    encryption_password = input("Escolha uma senha de criptografia (deve ser mantida em segredo): ")
    fernet = FernetHasher(FernetHasher.create_key(encryption_password))

    # Carregar senhas existentes
    passwords = {}
    if data_file.exists():
        with open(data_file, "r") as file:
            passwords = json.load(file)

    action = input("Você deseja (A)dicionar uma nova senha ou (R)ecuperar uma senha? ").strip().lower()

    if action == 'a':
        # Adicionando nova senha
        service = input("Digite o nome do serviço ou descrição da senha: ")
        password = input("Digite a senha a ser armazenada: ")
        encrypted_password = fernet.encrypt(password).decode()

        # Armazenar a senha criptografada
        passwords[service] = encrypted_password
        with open(data_file, "w") as file:
            json.dump(passwords, file)

        print(f"Senha para '{service}' armazenada com sucesso!")

    elif action == 'r':
        # Recuperando uma senha
        service = input("Digite o nome do serviço ou descrição da senha que deseja recuperar: ")
        if service in passwords:
            encrypted_password = passwords[service]
            decrypted_password = fernet.decrypt(encrypted_password)
            print(f"A senha para '{service}' é: {decrypted_password}")
        else:
            print(f"Nenhuma senha encontrada para '{service}'.")
    else:
        print("Opção inválida. Saindo.")

if __name__ == "__main__":
    main()
