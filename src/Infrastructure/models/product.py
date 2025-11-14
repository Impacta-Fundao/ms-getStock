from src import db
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

class Produto(db.Model):
    __tablename__ = "produtos"

    id = (Column(Integer, primary_key=True))
    nome = (Column(String(255), nullable=False))
    preco = (Column(Float, nullable=False))
    quantidade = (Column(Integer, nullable=False))
    imagem = (Column(String(255), nullable=False))
    status = (Column(Boolean, nullable=False))

    seller_id = (Column(Integer, ForeignKey("mercados.id", ondelete="CASCADE"), nullable=False))
    mercado = relationship("Mercado", back_populates="produtos")

    vendas = relationship("Venda", back_populates="produtos")
