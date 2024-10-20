import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import json

# Dados de teste para a tabela 'pessoa'
teste_pessoa = {
    "table": "pessoa",
    "tipo": "cliente",
    "cpf": 26670536072,
    "nome": "Megan Hayes",
    "sexo": "F",
    "data_nascimento": datetime.strptime("25/11/1929", "%d/%m/%Y").date(),
    "telefone": "+1-594-256-4669x3363",
    "email": "nicholas47@example.net",
    "senha": "_%5V@pl3Bp",
    "id_pessoa": 481,
}

# Dados de teste para a tabela 'endereco'
teste_endereco = {
    "table": "endereco",
    "id_pessoa": 813,
    "numero_casa": 23,
    "rua": "Pierce Radial",
    "bairro": "see",
    "cidade": "Benjaminfort",
    "estado": "PW",
    "cep": 98100945,
}

# Carrega as configurações de conexão do banco de dados a partir de um arquivo JSON
with open("config.json") as config_file:
    CONFIG = json.load(config_file)


def get_db_connection():
    """
    Estabelece uma conexão com o banco de dados MySQL usando as configurações fornecidas.

    Retorna:
        connection (mysql.connector.connection_cext.CMySQLConnection): Objeto de conexão se bem-sucedido.
        None: Se ocorrer um erro na conexão.
    """
    try:
        connection = mysql.connector.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG["database"],
        )
        return connection
    except mysql.connector.Error as err:
        print("Erro de Conexão com banco de dados: {}".format(err))
        return None


def execute_query(
    query,
    params=None,
    fetchall=True,
    dic=True,
    commit=False,
    debug=False,
    directly=False,
):
    """
    Executa uma consulta SQL genérica com parâmetros opcionais.

    Parâmetros:
        query (str): Consulta SQL a ser executada.
        params (tuple, opcional): Parâmetros para a consulta SQL.
        fetchall (bool, opcional): Se True, busca todos os resultados; caso contrário, busca apenas um.
        dic (bool, opcional): Se True, retorna os resultados como dicionários; caso contrário, como tuplas.
        commit (bool, opcional): Se True, confirma a transação.

    Retorna:
        dict: Dicionário contendo 'result', 'error' e 'last_id'.
              - 'result': Dados retornados pela consulta.
              - 'error': Indica se ocorreu um erro (True/False).
              - 'last_id': ID da última linha inserida (se aplicável).
    """
    connection = get_db_connection()
    if connection is None:
        if debug:
            print("Falha na Conexão")
        # Retorna um dicionário indicando falha na conexão
        return {"err": "Falha na Conexão", "error": True}

    cursor = connection.cursor(dictionary=dic)
    if directly:
        try:
            cursor.execute(query)

        except Exception as e:
            if debug:
                print(f"Erro: {e}")

            return {"error": True, "err": f"Erro geral: {e}"}
    else:
        try:
            cursor.execute(query, params)

        except Exception as e:
            if debug:
                print(f"Erro: {e}")

            return {"error": True, "err": f"Erro geral: {e}"}

    result = None

    if commit:
        # Confirma a transação no banco de dados
        connection.commit()
    if fetchall:
        # Busca todos os resultados da consulta
        result = cursor.fetchall()
    else:
        # Busca apenas um resultado da consulta
        result = cursor.fetchone()

    # Obtém o ID da última linha inserida, se aplicável
    last_id = cursor.lastrowid

    # Fecha o cursor e a conexão para liberar recursos
    cursor.close()
    connection.close()

    # Prepara a resposta a ser retornada
    resposta = {"result": result, "error": False, "last_id": last_id}

    if debug:
        print(resposta)
        print("Foi")

    return resposta


def Cadastro_SQL(dic, lista_ignorar=[], DEBUG=False):
    """
    Insere um registro em uma tabela especificada.

    Parâmetros:
        dic (dict): Dicionário contendo os dados a serem inseridos. Deve incluir a chave 'table'.
        lista_ignorar (list, opcional): Lista de chaves a serem ignoradas na inserção.
        DEBUG (bool, opcional): Se True, imprime a consulta SQL e os dados para depuração.

    Retorna:
        dict: Retorno da função execute_query contendo 'result', 'error' e 'last_id'.
    """
    # Adiciona a chave 'table' à lista de chaves a serem ignoradas
    lista_ignorar.append("table")

    # Inicia a construção da consulta SQL de inserção
    sql_query = f'INSERT INTO {dic["table"]} ('
    sql_data = ()
    cont = 0  # Contador para o número de colunas inseridas

    # Itera sobre as chaves do dicionário para construir as colunas e os dados
    for x in dic:
        if x not in lista_ignorar:
            sql_query += f"{x}, "
            sql_data += (dic[x],)
            cont += 1
    # Remove a última vírgula e espaço, e adiciona a parte de valores da consulta
    sql_query = sql_query[:-2] + ") VALUES (" + "%s, " * (cont - 1) + "%s)"

    if DEBUG:
        # Imprime a consulta SQL e os dados para depuração
        print(sql_query)
        print(sql_data)

    # Executa a consulta com commit=True para confirmar a transação
    return execute_query(sql_query, sql_data, commit=True)


# def Busca_SQL(dic, lista_ignorar=[], colunas=["*"],filter_data = True, all_data = False, f=True ,dictionary_response = True, DEBUG=False):
#     """
#     Realiza uma consulta SELECT em uma tabela com base nos critérios fornecidos.

#     Parâmetros:
#         dic (dict): Dicionário contendo os critérios de busca. Deve incluir a chave 'table'.
#         lista_ignorar (list, opcional): Lista de chaves a serem ignoradas na busca.
#         colunas (list, opcional): Lista de colunas a serem retornadas pela consulta.
#         DEBUG (bool, opcional): Se True, imprime a consulta SQL e os dados para depuração.

#     Retorna:
#         dict: Retorno da função execute_query contendo 'result', 'error' e 'last_id'.
#     """
#     # Adiciona a chave 'table' à lista de chaves a serem ignoradas
#     lista_ignorar.append("table")

#     # Inicia a construção da consulta SQL de seleção
#     sql_query = 'SELECT '
#     sql_data = ()
#     cont = 0  # Contador para o número de critérios de busca

#     all_data = list(dic.keys()) == ['table'] or all_data

#     if(all_data == True):
#         sql_query += f'* from {dic["table"]}'
#         if(filter_data):
#             sql_query += " where"
#     else:
#         for x in [x if x not in lista_ignorar else '' for x in dic.keys()]:
#             if(x != ''):
#                 sql_query += f'{x}, '
#         # Remove a última vírgula e espaço
#         sql_query = sql_query[:-2]
#         if(filter_data):
#             sql_query += f' FROM {dic["table"]} WHERE'
#         else:
#             sql_query += f' FROM {dic["table"]}'

#     if(filter_data):
#         # Itera sobre as chaves do dicionário para construir os critérios de busca
#         for x in dic:
#             if x not in lista_ignorar:
#                 sql_query += f" {x} = %s AND"
#                 sql_data += (dic[x],)
#                 cont += 1
#         # Remove o último ' AND'
#         sql_query = sql_query[:-4]

#     if DEBUG:
#         # Imprime a consulta SQL e os dados para depuração
#         print(dic)
#         print("Consulta;",sql_query,", dic:", dic)
#         print(sql_data)

#     # Executa a consulta com fetchall=False para obter apenas um registro
#     if(all_data):
#         return execute_query(sql_query, sql_data, dic=dictionary_response, fetchall=f)

#     return execute_query(sql_query, sql_data, dic=dictionary_response, fetchall=f)


def Busca_SQL(
    dic,
    lista_ignorar=[],
    colunas=["*"],
    filtros={},
    comparacoes={},
    filter_data=True,
    all_data=False,
    f=True,
    dictionary_response=True,
    DEBUG=False,
):
    """
    Realiza uma consulta SELECT em uma tabela com base nos critérios fornecidos.

    Parâmetros:
        dic (dict): Dicionário contendo os critérios de busca. Deve incluir a chave 'table'.
        lista_ignorar (list, opcional): Lista de chaves a serem ignoradas na busca.
        colunas (list, opcional): Lista de colunas a serem retornadas pela consulta (default: ["*"]).
        filtros (dict, opcional): Filtros de busca adicionais no formato {'coluna': valor}.
        comparacoes (dict, opcional): Critérios de comparação no formato {'coluna': 'operador'} (ex: {'idade': '>'}).
        filter_data (bool, opcional): Define se será aplicado um filtro à consulta (default: True).
        all_data (bool, opcional): Define se deve retornar todos os dados sem filtragem (default: False).
        fetchall (bool, opcional): Define se o retorno será uma lista de resultados ou apenas um único registro (default: True).
        dictionary_response (bool, opcional): Define se a resposta será em formato de dicionário (default: True).
        DEBUG (bool, opcional): Se True, imprime a consulta SQL e os dados para depuração (default: False).

    Retorna:
        dict: Retorno da função execute_query contendo 'result', 'error' e 'last_id'.
    """
    # Ignorar a chave 'table' nos filtros
    lista_ignorar.append("table")

    # Iniciar a construção da consulta SQL
    sql_query = "SELECT "
    sql_data = []

    # Definir colunas selecionadas
    if colunas == ["*"]:
        sql_query += "* "
    else:
        sql_query += ", ".join(colunas) + " "

    # Definir a tabela
    sql_query += f'FROM {dic["table"]} '

    # Definir filtros, se houver
    if filter_data and (filtros or comparacoes or dic):
        sql_query += "WHERE "

        # Adicionar filtros baseados nos valores de `dic`
        for chave, valor in dic.items():
            if chave not in lista_ignorar:
                sql_query += f"{chave} = %s AND "
                sql_data.append(valor)

        # Adicionar comparações (comparacoes)
        for coluna, operador in comparacoes.items():
            sql_query += f"{coluna} {operador} %s AND "
            sql_data.append(
                filtros[coluna]
            )  # Utiliza o valor correspondente nos filtros

        # Remover o último ' AND'
        sql_query = sql_query.rstrip(" AND ")

    # Imprimir a consulta SQL para depuração, se ativado
    if DEBUG:
        print("Consulta SQL:", sql_query)
        print("Dados SQL:", sql_data)

    # Executar a consulta SQL
    return execute_query(
        sql_query, tuple(sql_data), dic=dictionary_response, fetchall=f, debug=DEBUG
    )


def Busca_SQL_Join(
    base_table,
    join_conditions,
    colunas=["*"],
    filtros={},
    not_filtros={},
    comparacoes={},
    group_by=None,
    order_by=None,
    filter_data=True,
    all_data=False,
    fetchall=True,
    dictionary_response=True,
    DEBUG=True,
):
    """
    Realiza uma consulta SELECT com JOINs em uma tabela com base nos critérios fornecidos.

    Parâmetros:
        base_table (str): Nome da tabela base para a consulta.
        join_conditions (dict): Dicionário contendo as tabelas e condições de JOIN.
        colunas (list, opcional): Lista de colunas a serem retornadas pela consulta (default: ["*"]).
        filtros (dict, opcional): Filtros de busca adicionais no formato {'coluna': valor}.
        comparacoes (dict, opcional): Critérios de comparação no formato {'coluna': 'operador'}.
        group_by (str, opcional): Colunas para agrupar os resultados (default: None).
        order_by (str, opcional): Coluna para ordenar os resultados (default: None).
        filter_data (bool, opcional): Define se será aplicado um filtro à consulta (default: True).
        all_data (bool, opcional): Define se deve retornar todos os dados sem filtragem (default: False).
        fetchall (bool, opcional): Define se o retorno será uma lista de resultados ou apenas um único registro (default: True).
        dictionary_response (bool, opcional): Define se a resposta será em formato de dicionário (default: True).
        DEBUG (bool, opcional): Se True, imprime a consulta SQL e os dados para depuração (default: False).

    Retorna:
        dict: Retorno da função execute_query contendo 'result', 'error' e 'last_id'.
    """
    # Iniciar a construção da consulta SQL
    sql_query = "SELECT "
    sql_data = []

    # Definir colunas selecionadas
    if colunas == ["*"]:
        sql_query += "* "
    else:
        sql_query += ", ".join(colunas) + " "

    # Definir a tabela base
    sql_query += f"FROM {base_table} "

    # Adicionar as condições de JOIN
    for join_table, condition in join_conditions.items():
        sql_query += f"LEFT JOIN {join_table} ON {condition} "

    # Definir filtros, se houver
    if filter_data and (filtros or comparacoes):
        sql_query += "WHERE "

        # Adicionar filtros
        for coluna, valor in filtros.items():
            if valor == None:
                sql_query += f"{coluna} is %s AND "
            else:
                sql_query += f"{coluna} = %s AND "
            sql_data.append(valor)

        # Adicionar filtros reversos
        for coluna, valor in not_filtros.items():
            if valor == None:
                sql_query += f"{coluna} is not %s AND "
            else:
                sql_query += f"{coluna} != %s AND "
            sql_data.append(valor)

        # Adicionar comparações
        for coluna, operador in comparacoes.items():
            sql_query += f"{coluna} {operador} %s AND "
            sql_data.append(filtros[coluna])

        # Remover o último ' AND'
        sql_query = sql_query.rstrip(" AND ")

    # Adicionar cláusula GROUP BY, se houver
    if group_by:
        sql_query += f" GROUP BY {group_by} "

    # Adicionar cláusula ORDER BY, se houver
    if order_by:
        sql_query += f" ORDER BY {order_by} "

    # Imprimir a consulta SQL para depuração, se ativado
    if DEBUG:
        print("Consulta SQL:", sql_query)
        print("Dados SQL:", sql_data)

    # Executar a consulta SQL
    return execute_query(
        sql_query,
        tuple(sql_data),
        dic=dictionary_response,
        fetchall=fetchall,
        debug=DEBUG,
    )


def Delete_SQL(dic, lista_ignorar=[], DEBUG=False):
    lista_ignorar.append("table")

    # Inicia a construção da consulta SQL de Delete
    sql_query = f'Delete from {dic["table"]} where'
    sql_data = ()

    for x in dic:
        if x not in lista_ignorar:
            sql_query += f" {x} = '%s' and"
            sql_data += (dic[x],)

    # Remove o último and e espaço
    sql_query = sql_query[:-4]

    if DEBUG:
        # Imprime a consulta SQL e os dados para depuração
        print(dic)
        print(sql_query)
        print(sql_data)

    return execute_query(sql_query, sql_data, commit=True)


def Altera_SQL(dic, id_p, debug=False):
    sql_query = f"UPDATE {dic['table']} SET "
    sql_data = ()
    for x in dic:
        if x not in ["table", id_p]:
            sql_query += f"{x} = %s, "
            sql_data += (dic[x],)

    sql_query = sql_query[:-2]
    sql_query += " Where " + id_p + " = %s"
    sql_data += (dic[id_p],)
    if debug:
        print(sql_query)
        print(sql_data)
        print(dic)
    return execute_query(sql_query, sql_data, commit=True)


def Autentica_Login(dic):
    """
    Autentica um usuário com base nos critérios fornecidos.

    Parâmetros:
        dic (dict): Dicionário contendo os critérios de autenticação (por exemplo, 'email' e 'senha').

    Retorna:
        dict: Dicionário contendo os dados do usuário e 'login': True se autenticado com sucesso.
              Caso contrário, retorna {'login': False}.
    """
    # Realiza a busca no banco de dados com os critérios fornecidos
    results = Busca_SQL(dic, all_data=True, filter_data=True, f=False)
    # Verifica se a busca foi executada sem erros
    if Autentica_Dados(results):
        # Verifica se foi encontrado algum resultado
        if results["result"] is not None and results["result"] != []:
            # Adiciona a chave 'login' como True nos dados do usuário
            results["result"]["login"] = True
            return results["result"]
        else:
            # Retorna um dicionário indicando falha na autenticação
            return {"login": False}


def Autentica_Dados(response, silence=False):
    """
    Verifica se a resposta de uma consulta contém erros.

    Parâmetros:
        response (dict): Dicionário retornado pela função execute_query.

    Retorna:
        bool: True se sem erros, False caso contrário.
    """
    if response["error"]:
        # Imprime a mensagem de erro
        if silence == False:
            print("Erro: ", response["err"])
        return False
    return True
