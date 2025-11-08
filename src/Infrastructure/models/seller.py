from src import db
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Mercado(db.Model):
    __tablename__ = "mercados"
    
    id = (Column(Integer, primary_key=True))
    nome = (Column(String(255), nullable=False))
    cnpj = (Column(String(14), nullable=False))
    email = (Column(String(255), nullable=False))
    celular = (Column(String(11), nullable=False))
    senha = (Column(String(100), nullable=False))
    status = (Column(Boolean, nullable=False))

    produtos = relationship("Produto", back_populates="mercado", cascade="all, delete-orphan", passive_deletes=True)
    vendas = relationship("Venda", back_populates="mercado", cascade="all, delete-orphan", passive_deletes=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "senha": self.senha,
            "status": self.status
        }
