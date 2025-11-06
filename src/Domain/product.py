from dataclasses import dataclass

@dataclass
class ProductDomain:     
    nome: str
    preco: float
    quantidade: int
    status: bool
    imagem: str
