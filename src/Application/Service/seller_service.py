import os
from src.Domain.seller import SellerDomain
from src.Infrastructure.models.seller import Mercado
from src import db
from flask_jwt_extended import create_access_token, get_jwt_identity
import bcrypt
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
service_sid = os.environ["VERIFY_SERVICE_SID"]

client = Client(account_sid, auth_token)

class MercadoException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class SmsException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class AuthException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class SellerService:
    @staticmethod
    def create_seller(mercado_data):
        if not mercado_data: raise MercadoException("Nenhum dado fornecido")

        domain = SellerDomain(
            nome = mercado_data.get('nome') if mercado_data.get('nome') else False,
            cnpj = mercado_data.get('cnpj') if mercado_data.get('cnpj') else False,
            email = mercado_data.get('email') if mercado_data.get('email') else False,
            celular = mercado_data.get('celular') if mercado_data.get('celular') else False,
            senha = mercado_data.get('senha') if mercado_data.get('senha') else False,
            )
        
        data_itens = {"nome": domain.nome, 
                      "cnpj": domain.cnpj, 
                      "email": domain.email, 
                      "celular": domain.celular, 
                      "senha": domain.senha
                      }

        for k, v in data_itens.items():
            if not v: raise MercadoException(f"Passe um valor para o campo {k}")

        email_existente = Mercado.query.filter_by(email=domain.email).first()
        celular_existente = Mercado.query.filter_by(celular=domain.celular).first()
        
        if email_existente: raise MercadoException("Email já cadastrado")
        if celular_existente: raise MercadoException("Celular já cadastrado")

        domain.hash_password()

        client.verify.v2.services(service_sid).verifications.create(to=f"+55{domain.celular}", channel="sms")
        
        seller = Mercado(
            nome=domain.nome,
            cnpj=domain.cnpj,
            email=domain.email,
            celular=domain.celular,
            senha=domain.senha,
            status=domain.status
            )
        
        db.session.add(seller)
        db.session.commit()

        return seller.to_dict()
    
    @staticmethod
    def listar_mercados():
        mercados = Mercado.query.all()
        
        if not mercados: raise MercadoException("Não foram encontrados mercados cadastrados")

        return [{
            'id': mercado.id,
            'nome': mercado.nome,
            'cnpj': mercado.cnpj,
            'email': mercado.email,
            'celular': mercado.celular,
            'status': mercado.status
        } for mercado in mercados]
    
    @staticmethod
    def get_id(mercado_id):
        mercado = Mercado.query.get(mercado_id)

        if not mercado: raise MercadoException("Mercado não encontrado")
        
        return {
            'id': mercado.id,
            'nome': mercado.nome,
            'cnpj': mercado.cnpj,
            'email': mercado.email,
            'celular': mercado.celular,
            'status': mercado.status,
        }
    
    @staticmethod
    def deletar_mercado(mercado_id):
        mercado_id_jwt = get_jwt_identity()
        mercado = Mercado.query.get(mercado_id)

        if not mercado: raise MercadoException("Mercado não encontrado")
        if str(mercado_id) != mercado_id_jwt: raise MercadoException("Você não está autorizado a inativar este mercado")
        if not mercado.status: raise MercadoException("O mercado já se encontra inativado")

        mercado.status = False
            
        db.session.commit()
    
    @staticmethod
    def atualizar_mercado(mercado_id, mercado_data):
        mercado_id_jwt = get_jwt_identity()
        mercado = Mercado.query.get(mercado_id)

        if not mercado: raise MercadoException("Mercado não encontrado")
        if str(mercado_id) != mercado_id_jwt: raise MercadoException("Você não está autorizado a atualizar este mercado")
        if not mercado_data: raise MercadoException("Nenhum dado fornecido")
        
        data_itens = {
            'nome': mercado_data.get('nome'),
            'cnpj': mercado_data.get('cnpj'),
            'email': mercado_data.get('email'),
            'celular': mercado_data.get('celular'),
        }
        
        for k, v in data_itens.items():
            if not v:
                raise MercadoException(f"Passe um valor para o campo {k}")
        
        mercado.nome = data_itens['nome']
        cnpj_existente = Mercado.query.filter_by(cnpj=data_itens['cnpj']).first()
        if not cnpj_existente: mercado.cnpj = data_itens['cnpj']
        else: raise MercadoException("CNPJ já cadastrado")
        email_existente = Mercado.query.filter_by(email=data_itens['email']).first()
        if not email_existente: mercado.email = data_itens['email']
        else: raise MercadoException("Email já cadastrado")
        celular_existente = Mercado.query.filter_by(celular=data_itens['celular']).first()
        if not celular_existente: mercado.celular = data_itens['celular']
        else: raise MercadoException("Celular já cadastrado")
        
        db.session.commit()
        
        return {
            'id': mercado.id,
            'nome': mercado.nome,
            'cnpj': mercado.cnpj,
            'email': mercado.email,
            'celular': mercado.celular,
            'status': mercado.status
        }
        
    @staticmethod
    def atualizar_patch_mercado(mercado_id, mercado_data):
        mercado_id_jwt = get_jwt_identity()
        mercado = Mercado.query.get(mercado_id)

        if not mercado: raise MercadoException("Mercado não encontrado")
        if str(mercado_id) != mercado_id_jwt: raise MercadoException("Você não está autorizado a atualizar este mercado")
        if not mercado_data: raise MercadoException("Nenhum dado fornecido")
        
        if mercado_data.get('nome'): mercado.nome = mercado_data['nome']
        if mercado_data.get('cnpj'):
            cnpj_existente = Mercado.query.filter_by(cnpj=mercado_data['cnpj']).first()
            if not cnpj_existente: mercado.cnpj = mercado_data['cnpj']
            else: raise MercadoException("CNPJ já cadastrado")
        if mercado_data.get('email'):
            email_existente = Mercado.query.filter_by(email=mercado_data['email']).first()
            if not email_existente: mercado.email = mercado_data['email']
            else: raise MercadoException("Email já cadastrado")
        if mercado_data.get('celular'):
            celular_existente = Mercado.query.filter_by(celular=mercado_data['celular']).first()
            if not celular_existente: mercado.celular = mercado_data['celular']
            else: raise MercadoException("Celular já cadastrado")

        db.session.commit()
        
        return {
            'id': mercado.id,
            'nome': mercado.nome,
            'cnpj': mercado.cnpj,
            'email': mercado.email,
            'celular': mercado.celular,
            'status': mercado.status
        }

    @staticmethod
    def verificar_sms(data):
        if not data: raise SmsException("Nenhum dado fornecido")

        data_itens = {
                    "celular": data.get('celular'), 
                    "codigo": data.get('codigo')
                    }
        
        for k, v in data_itens.items():
            if not v: raise SmsException(f"Passe um valor para o campo {k}")
        
        mercado = Mercado.query.filter_by(celular=data_itens['celular']).first()

        if not mercado: raise SmsException("O número informado não existe cadastrado em nenhum mercado")
        if mercado.status: raise SmsException("O mercado já se encontra ativado")

        try:
            verification_check = client.verify.v2.services(service_sid).verification_checks.create(to=f"+55{data_itens['celular']}", code=data_itens['codigo'])
            
            if verification_check.status == "approved":
                mercado.status = True
                db.session.commit()
            elif verification_check.status == "pending":
                raise SmsException("O código informado está incorreto")
            else:
                raise SmsException(f"Status da verificação: {verification_check.status}")
        except SmsException as e:
            raise e
        except Exception:
            raise SmsException("Código inválido, expirado ou não solicitado")

    @staticmethod
    def authenticate(data):
        if not data: raise AuthException("Nenhum dado fornecido")

        data_itens = {
                    "email": data.get('email'), 
                    "senha": data.get('senha')
                    }
        
        for k, v in data_itens.items():
            if not v: raise AuthException(f"Passe um valor para o campo {k}")

        mercado = Mercado.query.filter_by(email=data_itens['email']).first()

        if not mercado: raise AuthException("Email incorreto")
        if not mercado.status: raise AuthException("O mercado está inativado")

        senha = mercado.senha
        
        if bcrypt.checkpw(data_itens['senha'].encode('utf-8'), senha.encode('utf-8')):
            access_token = create_access_token(identity=str(mercado.id))
            return access_token, mercado.id
        else: 
            raise AuthException("Senha incorreta")
