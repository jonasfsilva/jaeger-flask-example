import logging
import time
import json
from flask import Flask
from flask_restplus import Api, Resource
from flask import request
from jaeger_client import Config

# from models import UserModel
# from amqp import open_conn
# from amqp import produce_message
# from models import validate_payload


app = Flask(__name__)
api = Api(app=app)


# api_usuarios = UserModel.users_schema
# api.add_namespace(api_usuarios)


# @api_usuarios.route("/")
# class UserList(Resource):
    
#     @api_usuarios.expect(UserModel.model, validate=True)
#     def post(self): 
#         payload = json.loads(request.data)
        # custom_erros = validate_payload(payload)

        # if custom_erros:
        #     return custom_erros

        # produce_message("create", payload)
        # return {
        #     "message" : "Successfully Created User"
        # }, 201

def init_jaeger_trace():
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'jaeger',
                # 'reporting_port': 'your-reporting-port',
            },
            'logging': True,
        },  
        service_name='api',
        validate=True,
    )
    # this call also sets opentracing.tracer
    tracer = config.initialize_tracer()
    return tracer


def init_jaeger_tracer(service_name='api_service'):
    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'jaeger',
                # 'reporting_port': 'your-reporting-port',
            },
            'logging': True,
        },
        service_name=service_name, 
        validate=True
    )
    return config.initialize_tracer()


def main():
    print('******* START *******')
    tracer = init_jaeger_tracer()

    with tracer.start_span('TestSpan') as span:
        span.log_kv({'event': 'test message', 'life': 42})

    with tracer.start_span('ChildSpan', child_of=span) as child_span:
        span.log_kv({'event': 'down below'})


main()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    # Usuario já existe
    # Listar Produtos
    # Gerar Token do Cartao
    # Fazer Pagamento com Produto/Cartão Selecionados
    # Enviar Push Notification/Email
