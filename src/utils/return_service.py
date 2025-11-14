
class ReturnSeller():
    @staticmethod
    def sellers(seller):
        return {
            'id': seller.id,
            'nome': seller.nome,
            'cnpj': seller.cnpj,
            'email': seller.email,
            'celular': seller.celular,
            'status': seller.status,
        }

class ReturnProduct():
    @staticmethod
    def products(product):
        return {
            "id": product.id,
            "nome": product.nome,
            "preco": product.preco,
            "quantidade": product.quantidade,
            "imagem": product.imagem,
            "status": product.status
        }
    
class ReturnSale():
    @staticmethod
    def sales(sale):
        return {
            "id": sale.id,
            "produto_id": sale.produto_id,
            "preco_venda": sale.preco_venda,
            "quantidade": sale.quantidade,
            "total_venda": sale.total_venda,
            "data_venda": sale.data_venda
        }
