from src import db
from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship

class Venda(db.Model):
    __tablename__ = "vendas"

    id = (Column(Integer, primary_key=True))
    quantidade = (Column(Integer, nullable=False))
    preco_venda = (Column(Float, nullable=False))
    total_venda = (Column(Float, nullable=False))
    data_venda = (Column(DateTime, nullable=False))

    produto_id = (Column(Integer, ForeignKey("produtos.id"), nullable=False))
    produtos = relationship("Produto", back_populates="vendas")

    seller_id = (Column(Integer, ForeignKey("mercados.id", ondelete="CASCADE"), nullable=False))
    mercado = relationship("Mercado", back_populates="vendas")

    def to_dict(self):
        return {
            "id": self.id,
            "preco_venda": self.preco_venda,
            "quantidade": self.quantidade,
            "total_venda": self.total_venda,
            "data_venda": self.data_venda.strftime("%Y-%m-%d %H:%M:%S") if self.data_venda else None
        }
