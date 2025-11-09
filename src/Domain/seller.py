from dataclasses import dataclass
import bcrypt

@dataclass
class SellerDomain:     
    nome: str
    cnpj: str
    email: str
    celular: str
    senha: str
    status: bool = False
        
    def hash_password(self):
        self.senha = bcrypt.hashpw(self.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
