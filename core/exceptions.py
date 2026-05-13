from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status

class EstoqueInsuficienteError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Estoque insuficiente para realizar a venda.'
    default_code = 'estoque_insuficiente'

class ClienteComVendasError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Não é possível excluir um cliente que possui vendas registradas.'
    default_code = 'cliente_com_vendas'

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    return response