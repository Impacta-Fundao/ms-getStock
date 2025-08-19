from flask import request, jsonify, make_response
from src.Application.Service.seller_service import SellerService, MercadoException

class SellerController:
    @staticmethod
    def post_seller():
        try:
            data = request.get_json()
            requiredField = []
            
            nome=data['nome'] if data.get('nome') else None
            cnpj=data.get('cnpj') if data.get('cnpj') else None
            email=data.get('email') if data.get('email') else None
            celular=data.get('celular' if data.get('celular') else None)
            senha=data.get('senha') if data.get('senha') else None
            status=data.get(False)
            
            requiredField.append({"nome": nome, "cnpj":cnpj, "email": email, "celular":celular, "senha":senha,})
            for field in requiredField:
                for k,v in field.items():
                    if v is None:
                        return make_response(jsonify({"message": f"Passe um valor para o campo {k}"}), 400)
                    
            seller = SellerService.create_seller(nome,cnpj,email,celular,senha,status).to_dict()
            # resposta de sucesso
            return make_response(jsonify({ 
                "data": seller,
                "message": "Criado com sucesso"
                    }), 200)
        except MercadoException as e:
            return jsonify({"message": f"Erro na requisição {e.msg}"}, 500)
        
    @staticmethod
    def get_sellers():
        try:
            data = SellerService.listar_mercados()
            return make_response(jsonify({"data": data}), 200)
            
        
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro ao listar mercados: {str(e.msg)}"}), 500)

