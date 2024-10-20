from connect import *
from loja import *

# dados_user = Login(id_u=3)


# Menu_ADM(Login(id_u=1))
def obter_produtos_com_formas_pagamento():
    base_table = "estoque"
    join_conditions = {
        "produto_forma_pagamento": "estoque.id_produto = produto_forma_pagamento.id_produto",
        "forma_pagamento": "produto_forma_pagamento.id_forma_pagamento = forma_pagamento.id_forma_pagamento",
    }
    colunas = [
        "estoque.id_produto AS 'ID do Produto'",
        "estoque.nome AS 'Nome do Produto'",
        "forma_pagamento.nome AS 'Forma de Pagamento'",
        "produto_forma_pagamento.max_parcelas AS 'Máximo de Parcelas'",
    ]
    filtros = {}
    not_filtros = {}
    comparacoes = {}
    group_by = "estoque.id_produto, forma_pagamento.id_forma_pagamento"
    order_by = None
    filter_data = True
    all_data = False
    fetchall = True
    dictionary_response = True
    DEBUG = False
    dados = Busca_SQL_Join(
        base_table,
        join_conditions,
        colunas=colunas,
        filtros=filtros,
        not_filtros=not_filtros,
        comparacoes=comparacoes,
        group_by=group_by,
        order_by=order_by,
        filter_data=filter_data,
        all_data=all_data,
        fetchall=fetchall,
        dictionary_response=dictionary_response,
        DEBUG=DEBUG,
    )
    print(dados)
    exibir_tabela(
        dados,
        "Formas de Pagamento",
    )


obter_produtos_com_formas_pagamento()

# import datetime


# def Ajeita_Data(data_atual):
#     return "{}/{}/{}".format(data_atual.day, data_atual.month, data_atual.year)


# data = datetime.date.today()

# print(Ajeita_Data(data))

# data = data + datetime.timedelta(days=120)

# print(Ajeita_Data(data))
