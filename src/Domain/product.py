from dataclasses import dataclass

@dataclass
class ProductDomain:     
    nome: str
    preco: float
    quantidade: int
    imagem: str
    status: bool = True
