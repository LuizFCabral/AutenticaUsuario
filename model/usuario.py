from cryptography.fernet import Fernet

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def criptografar(self, senha):
        chave_cripto = Fernet.generate_key()
        fernet = Fernet(chave_cripto)
        return {"senha_cripto": fernet.encrypt(senha.encode()).decode(), "chave": chave_cripto.decode()}

    def descriptografar(self, senha, chave):
        fernet = Fernet(chave)
        return fernet.decrypt(senha.encode()).decode()