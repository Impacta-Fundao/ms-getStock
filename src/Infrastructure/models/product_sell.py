from src import db
from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

class Venda(db.Model):
    __tablename__ = "vendas"

    id = (Column(Integer, primary_key=True))
    quantidade_vendida = (Column(Integer, nullable=False))
    preco_venda = (Column(Float, nullable=False))

    produto_id = (Column(Integer, ForeignKey("produtos.id"), nullable=False))
    produto = relationship("Produto", back_populates="vendas")

    def to_dict(self):
        return {
            "id": self.id,
            "total_venda": self.quantidade_vendida,
            "preco_venda": self.preco_venda,
            "produto_id": self.produto_id
        }
