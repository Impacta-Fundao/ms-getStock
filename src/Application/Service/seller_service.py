from src.Domain.seller import SellerDomain
from src.Infrastructure.models.seller import Mercado
from src import db
import bcrypt

class MercadoException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class SellerService:
    
    @staticmethod
    def create_seller(seller_data: SellerDomain):
        email_existente = Mercado.query.filter_by(email=seller_data.email).first()
        celular_existente = Mercado.query.filter_by(celular=seller_data.celular).first()
        if email_existente:
            raise MercadoException("Email já cadastrado")
        if celular_existente:
            raise MercadoException("Celular já cadastrado")

        
        seller_data.hash_password()
        seller = Mercado(
            nome=seller_data.nome,
            cnpj=seller_data.cnpj,
            email=seller_data.email,
            celular=seller_data.celular,
            senha=seller_data.senha,
            status=seller_data.status
            )
        
        db.session.add(seller)
        db.session.commit()
        return seller
    
    @staticmethod
    def listar_mercados():
        data = Mercado.query.all()
        mercados_json = [{
            'id': mercado.id,
            'nome': mercado.nome,
            'cnpj': mercado.cnpj,
            'email': mercado.email,
            'celular': mercado.celular,
            'status': mercado.status
        } for mercado in data]
        
        return mercados_json
    
    @staticmethod
    def get_id(mercado_id):
        data = Mercado.query.get(mercado_id)

        if data is None: raise MercadoException("Esse mercado não está cadastrado")
        mercados_json = {
            'id': data.id,
            'nome': data.nome,
            'cnpj': data.cnpj,
            'email': data.email,
            'celular': data.celular,
            'status': data.status,
        } 
        
        return mercados_json
    
    @staticmethod
    def deletar_mercado(mercado_id):
        data = Mercado.query.get(mercado_id)
        if data is None:
            return None
        else:
            if data.status is False:
                return {"mensagem": "O mercado já se encontra inativado"}
            else:
                data.status = False
                
            db.session.commit()
            return {"mensagem": "Mercado inativado com sucesso"}
    
    @staticmethod
    def atualizar_mercado(mercado_id, mercado_data):
        data = Mercado.query.get(mercado_id)
        if data is None:
            raise MercadoException("Mercado não encontrado")
        
        required_fields = {
            'nome': mercado_data.get('nome'),
            'cnpj': mercado_data.get('cnpj'),
            'email': mercado_data.get('email'),
            'celular': mercado_data.get('celular'),
            'senha': mercado_data.get('senha')
        }
        
        for field, value in required_fields.items():
            if value is None:
                raise MercadoException(f"Passe um valor para o campo {field}")
        
        data.nome = required_fields['nome']
        data.cnpj = required_fields['cnpj']
        data.email = required_fields['email']
        data.celular = required_fields['celular']
        data.senha = required_fields['senha']
        if 'status' in mercado_data:
            data.status = mercado_data['status']
        
        db.session.commit()
        
        return {
            'id': data.id,
            'nome': data.nome,
            'cnpj': data.cnpj,
            'email': data.email,
            'celular': data.celular,
            'status': data.status
        }
        
    @staticmethod
    def atualizar_patch_mercado(mercado_id, mercado_data):
        data = Mercado.query.get(mercado_id)
        if data is None:
            raise MercadoException("Mercado não encontrado")
        if mercado_data.get('nome'):
            data.nome = mercado_data['nome']
        if mercado_data.get('cnpj'):
            data.cnpj = mercado_data['cnpj']
        if mercado_data.get('email'):
            data.email = mercado_data['email']
        if mercado_data.get('celular'):
            data.celular = mercado_data['celular']
        if mercado_data.get('senha'):
            data.senha = mercado_data['senha']
        if mercado_data.get('status'):
            data.status = mercado_data['status']
            
        db.session.commit()
        
        return {
            'id': data.id,
            'nome': data.nome,
            'cnpj': data.cnpj,
            'email': data.email,
            'celular': data.celular,
            'status': data.status
        }

    @staticmethod
    def authenticate(email_cadastrado, passw):
        seller = Mercado.query.filter_by(email=email_cadastrado).first()
        if not seller:
            return None
        if not seller.status:
            return False
        senha = seller.senha
        if bcrypt.checkpw(passw.encode('utf-8'), senha.encode('utf-8')):
            return seller
        return None

    @staticmethod
    def verificar_status_mercado(numero):
        mercado = Mercado.query.filter_by(celular=numero).first()
        if not mercado:
            return None
        if not mercado.status:
            return False
        return True

    @staticmethod
    def ativar_mercado(numero):
        mercado = Mercado.query.filter_by(celular=numero).first()
        mercado.status = True
        db.session.commit()
        return mercado.status
