from connect import *
import time
from pprint import pprint
from prettytable import PrettyTable
import copy
import requests
import datetime


def Perguntas_Respostas(pergs):
    respostas = []
    print()
    for x in pergs:
        print(x)
        respostas.append(input("Sua resposta:"))
    confirm = True
    while confirm:
        print("\nConfirme suas escolhas:")
        for x in range(1, len(respostas) + 1):
            print(f"{x} - {pergs[x-1]} - {respostas[x-1]}")
        desc = int(
            input(
                "Deseja mudar alguma escolha ?\n(Digite 0 caso não queira)\n\nSua resposta:"
            )
        )
        if desc != 0:
            print(pergs[desc - 1] + "\n")
            respostas[desc - 1] = input("Sua resposta:")
        else:
            return respostas


def Login(id_u=""):
    if id_u != "":
        return Autentica_Login({"table": "pessoa", "id_pessoa": id_u})
    print("=" * 30)
    print(" " * 10 + "TELA DE LOGIN")
    print("=" * 30)
    print()

    resposta = {"login": False}

    while resposta["login"] != True:
        print("\nFaça seu login:")
        user = {"table": "pessoa"}
        user["email"] = input("Seu email:")
        user["senha"] = input("Sua senha:")
        print("\nConfirmando Informações\n")

        resposta = Autentica_Login(user)
        if resposta["login"] == False:
            print("Informações de Login Inválidas !!")
            cad = int(
                input(
                    "Deseja Criar um Usuário ?\n(1) - Sim\n(2) - Não\n\nSua Escolha: "
                )
            )
            if cad == 1:
                Cadastro()
        else:
            break
    print("Bem Vindo " + resposta["nome"])
    return resposta


def Cadastro(funcionario=False, adm=False):
    print("=" * 30)
    print(" " * 7 + "TELA DE CADASTRO")
    print("=" * 30)
    print()

    resposta = {"cadastrado": False}
    while resposta["cadastrado"] == False:
        nome = input("Defina seu nome:")
        email = input("Defina seu email:")
        senha = input("Defina sua senha:")
        confirm_senha = input("Confirme sua senha:")
        onepiece = int(
            input("Assiste One Piece ?\n(1) - Sim\n(2) - Não\nSua Escolha: ")
        )
        flamengo = int(input("Mengão ?\n(1) - Sim\n(2) - Não\nSua Escolha: "))

        cpf = input("Digite seu CPF (Apenas Numeros):")

        while True:
            try:
                data = input("Digite sua data de nascimento (dd/mm/aaaa): ")
                data_nascimento = datetime.datetime.strptime(data, "%d/%m/%Y")
            except:
                print("Data de Nascimento Invalida, digite no formato DD/MM/AAAA")
            else:
                break
        telefone = input("Digite seu Telefone (Apenas Numeros): ")

        onepiece = True if onepiece == 1 else False
        flamengo = True if onepiece == 1 else False
        print("\nConfirmando Informações\n")  # checkpoint

        if (
            Valida_Cadastro(
                {"nome": nome, "email": email, "senha": senha, "senha2": confirm_senha}
            )
            == False
        ):
            if funcionario:
                dados = Cadastro_SQL(
                    {
                        "table": "pessoa",
                        "tipo": "funcionario",
                        "nome": nome,
                        "email": email,
                        "senha": senha,
                        "is_flamengo": flamengo,
                        "is_onepiece": onepiece,
                        "data_nascimento": data_nascimento,
                        "cpf": cpf,
                        "telefone": telefone,
                    }
                )
            elif adm:
                dados = Cadastro_SQL(
                    {
                        "table": "pessoa",
                        "tipo": "adm",
                        "nome": nome,
                        "email": email,
                        "senha": senha,
                        "is_flamengo": flamengo,
                        "is_onepiece": onepiece,
                        "data_nascimento": data_nascimento,
                        "cpf": cpf,
                        "telefone": telefone,
                    }
                )
            else:
                dados = Cadastro_SQL(
                    {
                        "table": "pessoa",
                        "nome": nome,
                        "email": email,
                        "senha": senha,
                        "is_flamengo": flamengo,
                        "is_onepiece": onepiece,
                        "data_nascimento": data_nascimento,
                        "cpf": cpf,
                        "telefone": telefone,
                    }
                )
            if Autentica_Dados(dados):
                if funcionario:
                    salario = float(
                        input("Defina o Salario do Funcionario: ").replace(",", ".")
                    )
                    Cadastro_SQL(
                        {
                            "table": "funcionario",
                            "cod_funcionario": dados["last_id"],
                            "salario": salario,
                        }
                    )
                    print("Cadastro de Funcionario Concluido !")
                    break

                else:
                    Cadastro_SQL({"table": "cliente", "cod_cliente": dados["last_id"]})
                print("Confirme agora seu Login:\n\n")
                break


def Valida_Cadastro(dic):
    error = False

    senhas_iguais = (dic["senha"] == dic["senha2"]) == False
    lista_email_igual = Busca_SQL({"table": "pessoa", "email": dic["email"]})
    if lista_email_igual["error"] == False:
        if lista_email_igual["result"] == []:
            email_duplicado = False
        else:
            email_duplicado = True
    else:
        print("Erro: " + lista_email_igual["err"])
        error = True

    if email_duplicado:
        print("Já existe um usuario com este email")
    if senhas_iguais:
        print("As senhas devem ser iguais !")
    print()

    error += senhas_iguais + email_duplicado
    return error


def Menu_Usuario(id_C=""):
    if id_C != "":
        login = True
        dados_cliente = Login(id_u=id_C)
    else:
        login = False
    while True:
        print("=" * 30)
        print(" " * 10 + "LOJA DE ROUPA")
        print("=" * 30)
        print()

        print("Selecione uma opção (0/Sair): ")
        selecao = int(
            input(
                "(1) - Abrir Loja\n(2) - Faturas\n(3) - Produtos Favoritos\n(4) - Vizualizar Carrinho de Compras\n\nSua Escolha:"
            )
        )
        if selecao == 1:
            while True:
                if Abrir_Loja():
                    print("Selecione uma Opção: ")
                    selecao = int(
                        input(
                            "(1) - Comprar Produto\n(2) - Favoritar Produto\n(3) - Adicionar ao Carrinho\n\nSua Escolha:"
                        )
                    )
                    if selecao == 0:
                        break
                    elif login == False:
                        selecao = int(
                            input(
                                "Para isso é necessário que o cliente Faça Login\nDeseja Fazer Login ?\n(1) - Sim\n(2) - Não\n\nSua Escolha: "
                            )
                        )
                        if selecao == 1:
                            dados_cliente = Login()
                            if dados_cliente["tipo"] == "adm":
                                Menu_ADM(dados_cliente)
                                break

                            elif dados_cliente["tipo"] == "funcionario":
                                Menu_Funcionario(dados_cliente)
                                break

                            login = True
                        else:
                            continue
                    elif selecao == 1:
                        Comprar_Produto(dados_cliente["id_pessoa"])
                    elif selecao == 2:
                        Favorita_Produto(dados_cliente["id_pessoa"])
                    elif selecao == 3:
                        id_prod = int(input("Defina o ID do produto: "))
                        if (
                            Busca_SQL(
                                {"table": "estoque", "id_produto": id_prod}, f=False
                            )["result"]
                            != None
                        ):
                            quantidade = int(input("Defina a Quantidade desejada: "))
                            if quantidade > 0:
                                dados_p = Busca_SQL(
                                    {
                                        "table": "carrinho_compras",
                                        "id_produto": id_prod,
                                        "id_pessoa": dados_cliente["id_pessoa"],
                                    },
                                    f=False,
                                )
                                if dados_p["result"] != None:
                                    Altera_SQL(
                                        {
                                            "table": "carrinho_compras",
                                            "id_produto": id_prod,
                                            "quantidade": dados_p["result"][
                                                "quantidade"
                                            ]
                                            + quantidade,
                                        },
                                        "id_produto",
                                    )
                                else:
                                    Cadastro_SQL(
                                        {
                                            "table": "carrinho_compras",
                                            "id_pessoa": dados_cliente["id_pessoa"],
                                            "id_produto": id_prod,
                                            "quantidade": quantidade,
                                        }
                                    )
                            else:
                                print("Quantidade Invalida")
                        else:
                            print("ID Inválido")
                else:
                    break
        elif selecao == 0:
            return None
        elif login == False:
            selecao = int(
                input(
                    "Para isso é necessário que o cliente Faça Login\nDeseja Fazer Login ?\n(1) - Sim\n(2) - Não\n\nSua Escolha: "
                )
            )
            if selecao == 1:
                dados_cliente = Login()
                if dados_cliente["tipo"] == "adm":
                    Menu_ADM(dados_cliente)
                    break

                elif dados_cliente["tipo"] == "funcionario":
                    Menu_Funcionario(dados_cliente)
                    break

                login = True
            else:
                continue
        elif selecao == 2:
            base_table = "parcelas"
            join_conditions = {
                "pedido": "parcelas.id_pedido = pedido.id_pedido",
                "pessoa": "pedido.id_cliente = pessoa.id_pessoa",
            }
            colunas = [
                "parcelas.id_parcela",
                "parcelas.id_pedido",
                "parcelas.numero_parcela",
                "parcelas.data_vencimento",
                "parcelas.valor",
                "parcelas.status",
            ]
            filtros = {"pessoa.id_pessoa": dados_cliente["id_pessoa"]}
            order_by = "parcelas.data_vencimento"

            result = Busca_SQL_Join(
                base_table=base_table,
                join_conditions=join_conditions,
                colunas=colunas,
                filtros=filtros,
                order_by=order_by,
            )
            if exibir_tabela(result, "Parcelas do Cliente"):
                selecao = int(
                    input(
                        "Deseja pagar alguma fatura ?\n(1) - Sim\n(2) - Não\nSua Escolha: "
                    )
                )
                if selecao == 1:
                    while True:
                        id_parcela = int(input("Ddefina o ID da fatura (0/Sair):"))
                        if id_parcela == 0:
                            break
                        else:
                            # Definindo a tabela base e as condições de junção
                            base_table = "parcelas AS pa"
                            join_conditions = {
                                "pedido AS ped": "pa.id_pedido = ped.id_pedido",
                                "pessoa AS p": "ped.id_cliente = p.id_pessoa",
                            }

                            # Definindo as colunas a serem selecionadas
                            colunas = [
                                'p.id_pessoa AS "ID da Pessoa"',
                                'pa.id_parcela AS "ID da Parcela"',
                            ]

                            # Filtros para a consulta
                            filtros = {"pa.status": "Pendente"}

                            # Realizando a consulta usando a função Busca_SQL_Join
                            result = Busca_SQL_Join(
                                base_table=base_table,
                                join_conditions=join_conditions,
                                colunas=colunas,
                                filtros=filtros,
                            )

                            if Verifica_ID(
                                "parcelas",
                                [
                                    ["ID da Parcela", id_parcela],
                                    ["ID da Pessoa", dados_cliente["id_pessoa"]],
                                ],
                                data=result,
                            ):
                                Altera_SQL(
                                    {
                                        "table": "parcelas",
                                        "id_parcela": id_parcela,
                                        "status": "Pago",
                                    },
                                    "id_parcela",
                                )
                                print("Pago")
                                break
                pass
        elif selecao == 3:
            while True:
                if Produtos_Favoritos(dados_cliente["id_pessoa"]):
                    selecao = int(
                        input(
                            "(1) - Desfavoritar\n(2) - Comprar Produto\n(3) - Menu Anterior\n\nSua Escolha:"
                        )
                    )
                    if selecao == 1:
                        id_produto = int(input("Defina o ID do produto: "))
                        response = Delete_SQL(
                            {
                                "table": "usuario_favorita_produto",
                                "id_cliente": dados_cliente["id_pessoa"],
                                "id_produto": id_produto,
                            }
                        )
                        if Autentica_Dados(response):
                            print("Produto desfavoritado com sucesso")
                        else:
                            print("Erro ao Desfavoritar Produto")

                    elif selecao == 2:
                        Comprar_Produto(dados_cliente["id_pessoa"])

                    elif selecao == 0:
                        break
                else:
                    break
        elif selecao == 4:
            if not Vizualizar_carrinho(dados_cliente["id_pessoa"]):
                selecao = int(
                    input(
                        "Oque deseja fazer ? (0/Sair)\n(1) - Comprar Carrinho\n(2) - Remover Item do Carrinho\n\nSua Escolha: "
                    )
                )
                if selecao == 0:
                    continue
                elif selecao == 1:
                    id_produtos = Busca_SQL(
                        {
                            "table": "carrinho_compras",
                            "id_pessoa": dados_cliente["id_pessoa"],
                        }
                    )
                    if id_produtos["result"] == []:
                        print("Não Há produtos no seu carrinho")
                    else:
                        id_produtos = id_produtos["result"]
                        sair = False
                        for x in id_produtos:
                            if x["quantidade"] > Verifica_estoque(x["id_produto"]):
                                escolha = int(
                                    input(
                                        f"Produto {Busca_SQL({'table':'estoque', 'id_produto':x['id_produto']}, colunas=['nome'], f=False)['result']['nome']} Não disponível na quantidade desejada\nAlterando de {x['quantidade']} -> {Verifica_estoque(x['id_produto'])}\n(1) - Aceito\n(2) - Não, Cancelar\nSua Escolha:"
                                    )
                                )
                                if escolha == 2:
                                    sair = True
                                    break
                                x["quantidade"] = Verifica_estoque(x["id_produto"])
                        if sair == True:
                            continue
                        while True:
                            exibir_tabela(
                                Busca_SQL(
                                    {"table": "forma_pagamento"}, filter_data=False
                                ),
                                "Formas de Pagamento",
                            )
                            id_forma_pag = int(
                                input("Defina o ID da forma de Pagamento: ")
                            )
                            if (
                                Verifica_ID(
                                    "forma_pagamento",
                                    [["id_forma_pagamento", id_forma_pag]],
                                )
                                == False
                            ):  # CheckPoint
                                print("Forma de Pagamento Invalida")
                                continue
                            else:
                                info_pag = Busca_SQL(
                                    {
                                        "table": "forma_pagamento",
                                        "id_forma_pagamento": id_forma_pag,
                                    },
                                    f=False,
                                )["result"]
                            parcelas = 1
                            if info_pag["permite_parcelamento"]:
                                parcelas = int(
                                    input("Defina a Quantidade de Parcelas: ")
                                )
                                if parcelas > 12 or parcelas < 1:
                                    print(f"Quantidade Invalida de Parcelas (Max:12)")
                                    continue

                            end = 0
                            while end == 0:
                                enderecos = Busca_SQL(
                                    {
                                        "table": "endereco",
                                        "id_pessoa": dados_cliente["id_pessoa"],
                                    }
                                )
                                if Autentica_Dados(enderecos):
                                    if (
                                        enderecos["result"] == None
                                        or enderecos["result"] == []
                                    ):
                                        print(
                                            "\nNenhum Endereco Associado, Registre um Endereco:"
                                        )
                                        Registra_Endereco(dados_cliente["id_pessoa"])
                                        continue
                                    else:
                                        print("\nConfirme seu Endereço:")
                                        exibir_tabela(
                                            enderecos, "Endereços Cadastrados"
                                        )
                                        endereco_cliente = int(
                                            input("Defina o ID do seu Endereco: ")
                                        )
                                        if Verifica_ID(
                                            "endereco",
                                            [["id_endereco", endereco_cliente]],
                                        ):
                                            print(id_produtos)
                                            Executa_Compra(
                                                dados_cliente["id_pessoa"],
                                                endereco_cliente,
                                                parcelas,
                                                id_forma_pag,
                                                {
                                                    c["id_produto"]: (
                                                        c["quantidade"],
                                                        Busca_SQL(
                                                            {
                                                                "table": "estoque",
                                                                "id_produto": c[
                                                                    "id_produto"
                                                                ],
                                                            },
                                                            f=False,
                                                        )["result"]["preco"],
                                                    )
                                                    for c in id_produtos
                                                    if (c["quantidade"] > 0)
                                                },
                                            )
                                            print("Compra Concluida")
                                            Delete_SQL(
                                                {
                                                    "table": "carrinho_compras",
                                                    "id_pessoa": dados_cliente[
                                                        "id_pessoa"
                                                    ],
                                                }
                                            )

                                            break
                                        else:
                                            op = int(
                                                input(
                                                    "Opção de Endereco Não Encontrada, desseja Cadastrar um novo ?\n(1) - Sim\n(2) - Não\n\nSua Escolha: "
                                                )
                                            )
                                            if op == 1:
                                                Registra_Endereco(
                                                    dados_cliente["id_pessoa"]
                                                )
                            break
                elif selecao == 2:
                    id_carrinho = int(input("Defina o ID do produto: "))
                    if Verifica_ID(
                        "carrinho_compras",
                        [
                            ["id_produto", id_carrinho],
                            ["id_pessoa", dados_cliente["id_pessoa"]],
                        ],
                    ):
                        response = Delete_SQL(
                            {
                                "table": "carrinho_compras",
                                "id_pessoa": dados_cliente["id_pessoa"],
                                "id_produto": id_carrinho,
                            }
                        )
                        if Autentica_Dados(response):
                            print("Produto Removido do Carrinho com Sucesso !\n")

    if login:
        return dados_cliente


def Verifica_estoque(id_prod):
    dados = Busca_SQL({"table": "estoque", "id_produto": id_prod}, f=False)
    if Autentica_Dados(dados):
        if dados["result"] == None:
            return 0
        else:
            return dados["result"]["quantidade"]


def Vizualizar_carrinho(id_pessoa):
    # Definindo a tabela base e as condições de junção
    base_table = "carrinho_compras AS cc"
    join_conditions = {"estoque AS e": "cc.id_produto = e.id_produto"}

    # Definindo as colunas a serem selecionadas
    colunas = [
        'e.id_produto AS "ID do Produto"',
        'e.nome AS "Nome do Produto"',
        'cc.quantidade AS "Quantidade"',
        'e.preco AS "Preco Unitario"',
    ]

    # Filtros para a consulta
    filtros = {"cc.id_pessoa": id_pessoa}

    # Realizando a consulta usando a função Busca_SQL_Join
    result = Busca_SQL_Join(
        base_table=base_table,
        join_conditions=join_conditions,
        colunas=colunas,
        filtros=filtros,
    )
    return exibir_tabela(
        result,
        "Carrinho de Compras",
        total=("Quantidade", "Preco Unitario"),
    )


def Verifica_ID(table, id_prod, data="", debug=False):
    if data != "":
        for x in data["result"]:
            if sum(x[cond[0]] == cond[1] for cond in id_prod) == len(
                id_prod
            ):  #:x[id_prod[0]] == id_prod[1]:
                return True
        return False
    ids = {x[0]: x[1] for x in id_prod}
    ids["table"] = table

    ids = Busca_SQL(ids, f=False)

    if debug:
        print(ids)
        Autentica_Dados(ids)
    return ids["result"] != None


def Apaga_Carrinho(id_cliente):
    execute_query(
        f"Delete from carrinho_compras where id_cliente = {id_cliente}",
        directly=True,
        commit=True,
    )


def Abrir_Loja():
    print("\nLojinha do Joao:")
    dados_estoque = Busca_SQL(
        {"table": "estoque"},
        filtros={"quantidade": 0},
        comparacoes={"quantidade": ">"},
        DEBUG=False,
    )
    if Autentica_Dados(dados_estoque):
        return exibir_tabela(dados_estoque, "Produtos da Loja")


def Comprar_Produto(id_cliente):
    while True:
        id_produto = int(input("Defina o ID do Produto: "))
        quantidade = int(input("Defina a Quantidade desejada do Produto: "))
        dados_produto = Busca_SQL(
            {"table": "estoque", "id_produto": id_produto},
            colunas=["quantidade", "preco"],
            f=False,
        )
        if Autentica_Dados(dados_produto, silence=True):
            if dados_produto["result"] != None:
                if dados_produto["result"]["quantidade"] < quantidade or quantidade < 1:
                    print(
                        "Quantidade Inválida do Produto (Max:",
                        dados_produto["result"]["quantidade"],
                        ")",
                    )
                else:
                    preco = dados_produto["result"]["preco"]
                    break
            else:
                print("ID de produto Invalido")
    print("Como deseja comprar o produto ?")
    dados = execute_query(
        f"""SELECT 
    e.id_produto AS id_produto,
    e.nome AS nome_produto,
    e.preco AS preco_produto,
    fp.id_forma_pagamento AS id_forma_pagamento,
    fp.nome AS nome_forma_pagamento
FROM 
    estoque e
JOIN 
    produto_forma_pagamento pfp ON e.id_produto = pfp.id_produto
JOIN 
    forma_pagamento fp ON pfp.id_forma_pagamento = fp.id_forma_pagamento
WHERE 
    e.id_produto = {id_produto};
""",
        directly=True,
    )
    exibir_tabela(dados, "Formas de Pagamento")

    while True:

        id_forma_pag = int(input("Defina o ID da forma de Pagamento: "))
        if (
            sum(
                [
                    1 if x["id_forma_pagamento"] == id_forma_pag else 0
                    for x in dados["result"]
                ]
            )
            != 1
        ):
            print("Forma de Pagamento Invalida")
            continue
        else:
            info_pag = Busca_SQL(
                {
                    "table": "forma_pagamento",
                    "id_forma_pagamento": id_forma_pag,
                },
                f=False,
            )["result"]
            parcelas = 1
            if info_pag["permite_parcelamento"]:
                parcelas = int(input("Defina a Quantidade de Parcelas: "))
                info_pag = Busca_SQL(
                    {"table": "produto_forma_pagamento", "id_produto": dados_produto}
                )["result"]
                if parcelas > info_pag["max_parcelas"] or parcelas < 1:
                    print(
                        f"Quantidade Invalida de Parcelas (Max:{info_pag['max_parcelas']})"
                    )
                    continue

            end = 0
            while end == 0:
                enderecos = Busca_SQL({"table": "endereco", "id_pessoa": id_cliente})
                if Autentica_Dados(enderecos):
                    if enderecos["result"] == None or enderecos["result"] == []:
                        print("\nNenhum Endereco Associado, Registre um Endereco:")
                        Registra_Endereco(id_cliente)
                        continue
                    else:
                        print("\nConfirme seu Endereço:")
                        exibir_tabela(enderecos, "Endereços Cadastrados")
                        endereco_cliente = int(input("Defina o ID do seu Endereco: "))
                        if (
                            sum(
                                [
                                    1 if x["id_endereco"] == endereco_cliente else 0
                                    for x in enderecos["result"]
                                ]
                            )
                            == 1
                        ):
                            Executa_Compra(
                                id_cliente,
                                endereco_cliente,
                                parcelas,
                                id_forma_pag,
                                {id_produto: (quantidade, preco)},
                            )
                            print("Compra Concluida")
                            break
                        else:
                            op = int(
                                input(
                                    "Opção de Endereco Não Encontrada, desseja Cadastrar um novo ?\n(1) - Sim\n(2) - Não\n\nSua Escolha: "
                                )
                            )
                            if op == 1:
                                Registra_Endereco(id_cliente)
            break
    return


def Executa_Compra(
    id_cliente, endereco_cliente, parcelas, id_forma_pag, lista_produtos
):
    dados_cliente = Busca_SQL({"table": "pessoa", "id_pessoa": id_cliente})["result"][0]
    print(dados_cliente)
    desconto = 1
    if (
        dados_cliente["is_flamengo"]
        or dados_cliente["is_onepiece"]
        or "souza" in dados_cliente["nome"].lower().split(" ")
        or "sousa" in dados_cliente["nome"].lower().split(" ")
    ):
        desconto = 0.9
    dados_rotulos = [
        "table",
        "id_cliente",
        "id_endereco",
        "id_forma_pagamento",
        "total",
        "numero_parcelas",
    ]
    total = sum(
        [
            float(quantidade[0]) * float(quantidade[1]) * desconto
            for prod, quantidade in lista_produtos.items()
        ]
    )
    dados_values = [
        "pedido",
        id_cliente,
        endereco_cliente,
        id_forma_pag,
        total,
        parcelas,
    ]

    dados = {dados_rotulos[x]: dados_values[x] for x in range(len(dados_rotulos))}
    response = Cadastro_SQL(dados, DEBUG=False)
    id_pedido = response["last_id"]
    dados_rotulos_pedido_produto = [
        "table",
        "id_pedido",
        "id_produto",
        "quantidade",
        "preco_unitario",
    ]
    dados_rotulos_parcelas = [
        "table",
        "id_pedido",
        "numero_parcela",
        "data_vencimento",
        "valor",
    ]
    for prod, quantidade_preco in lista_produtos.items():
        dados_values_pedido_produto = [
            "pedido_produto",
            id_pedido,
            prod,
            quantidade_preco[0],
            float(quantidade_preco[1]) * desconto,
        ]

        quantidade_produto = Busca_SQL(
            {"table": "estoque", "id_produto": prod},
            colunas=["quantidade"],
            f=False,
            DEBUG=False,
        )["result"]["quantidade"]

        response = Altera_SQL(
            {
                "table": "estoque",
                "id_produto": prod,
                "quantidade": quantidade_produto - quantidade_preco[0],
            },
            "id_produto",
            debug=False,
        )
        Autentica_Dados(response)

        response = Cadastro_SQL(
            {
                dados_rotulos_pedido_produto[x]: dados_values_pedido_produto[x]
                for x in range(len(dados_values_pedido_produto))
            },
            DEBUG=False,
        )
        Autentica_Dados(response)

        for x in range(parcelas):
            dados_values_parcelas = [
                "parcelas",
                id_pedido,
                x + 1,
                datetime.date.today() + datetime.timedelta(days=30 * (x + 1)),
                total / parcelas,
            ]
            Autentica_Dados(
                Cadastro_SQL(
                    {
                        dados_rotulos_parcelas[x]: dados_values_parcelas[x]
                        for x in range(len(dados_rotulos_parcelas))
                    }
                )
            )


def Registra_Endereco(id_cliente):
    cep = (
        input("Defina Seu CEP (Apenas Numeros): ")
        .replace("-", "")
        .replace(".", "")
        .replace(" ", "")
    )
    rua = int(input("Defina o numero da sua casa: "))
    if len(cep) == 8:
        try:
            link = f"https://viacep.com.br/ws/{cep}/json/"
            requisicao = requests.get(link)
            dic_requisicao = requisicao.json()
        except:
            return Registra_Endereco_Manual(id_cliente)
        else:
            if (
                dic_requisicao == {}
                or dic_requisicao == None
                or "erro" in dic_requisicao
            ):
                return Registra_Endereco_Manual(id_cliente)
        print("Confirme suas Informações")
        dados = {}
        print(dic_requisicao)
        dados["result"] = [
            {
                "cep": cep,
                "rua": dic_requisicao["logradouro"],
                "bairro": dic_requisicao["bairro"],
                "cidade": dic_requisicao["localidade"],
                "estado": dic_requisicao["uf"],
            }
        ]
        exibir_tabela(dados, "Suas Informações de Localidade")
        confirm = int(input("Confirma as informações ? (1/Sim)\nSua Escolha: "))
        if confirm == 1:
            dados = dados["result"][0]
            dados["id_pessoa"] = id_cliente
            dados["table"] = "endereco"
            dados["numero_casa"] = rua
            response = Cadastro_SQL(dados, DEBUG=False)
            if Autentica_Dados(response):
                print("Dados de Endereço Salvos")
        else:
            Registra_Endereco_Manual(id_cliente)
    else:
        print("CEP Invalido")


def Registra_Endereco_Manual(id_cliente):
    dados = Perguntas_Respostas(
        [
            "Defina seu CEP: ",
            "Defina sua Rua: ",
            "Defina seu Bairro: ",
            "Defina sua Cidade: ",
            "Defina seu Estado: ",
            "Defina o Nº da sua Casa: ",
        ]
    )
    dados.extend([id_cliente, "endereco"])
    rotulos = [
        "cep",
        "rua",
        "bairro",
        "cidade",
        "estado",
        "numero_casa",
        "id_pessoa",
        "table",
    ]
    dados = {rotulos[x]: dados[x] for x in range(len(dados))}
    repsonse = Cadastro_SQL(dados)
    if Autentica_Dados(repsonse):
        print("Endereco Cadastrado")


def Favorita_Produto(id_cliente):
    id_produto = int(input("Defina o ID do produto:"))
    dados = Cadastro_SQL(
        {
            "table": "usuario_favorita_produto",
            "id_cliente": id_cliente,
            "id_produto": id_produto,
        }
    )
    if Autentica_Dados(dados):
        print("Produto Favoritado com Sucesso")


def Produtos_Favoritos(id_cliente):
    id_produtos = Busca_SQL(
        {
            "table": "usuario_favorita_produto",
            "id_cliente": id_cliente,
        }
    )  # Parei nessa linha, fazer a busca por produtos favoritados no id do usuario na lista de estoque e retornar as informaç~çoes completas dos produtos
    if Autentica_Dados(id_produtos):
        id_produtos = id_produtos["result"]
        if id_produtos == []:
            print("Voce não tem produtos favoritados")
            return False
        dados_produtos = [
            Busca_SQL({"table": "estoque", "id_produto": x["id_produto"]})
            for x in id_produtos
        ]
        dados_produtos = [produto["result"][0] for produto in dados_produtos]
        dados_produtos_estoque = [
            produto for produto in dados_produtos if produto["quantidade"] > 0
        ]
        if dados_produtos_estoque == []:
            print("Voce não tem produtos favoritados em estoque")
        # Criando uma tabela
        tabela = PrettyTable()
        tabela.field_names = list(dados_produtos[0].keys()) + ["Data Favoritado"]
        # Exibindo a tabela
        for x in range(len(dados_produtos)):
            tabela.add_row(
                list(dados_produtos[x].values())
                + [id_produtos[x]["data_cadastro"].strftime("%d/%m/%Y %H:%M:%S")]
            )

        print(tabela)
        time.sleep(1)
        return True


def Menu_Funcionario(user):
    while True:
        print("=" * 30)
        print(" " * 7 + "ESTOQUE DE ROUPA")
        print("=" * 30)
        print()

        Exibir_Estoque()

        print("Selecione uma opção (0/Sair): ")
        selecao = int(
            input(
                "(1) - Modificar Estoque\n(2) - Adicionar Produto\n(3) - Remover Produto\n(4) - Efetivar Compras\n\n Sua Escolha: "
            )
        )
        if selecao == 1:
            Modificar_Estoque()
            pass
        elif selecao == 2:
            Adicionar_Produto()
            pass
        elif selecao == 3:
            Remover_Produto()
            pass
        elif selecao == 4:
            Efetivar_Compra(user["id_pessoa"])
            pass
        elif selecao == 0:
            break


def Exibir_Compras_Efetivadas(reverse=False):
    base_table = "pedido"
    join_conditions = {
        "pessoa": "pedido.id_cliente = pessoa.id_pessoa",
        "forma_pagamento": "pedido.id_forma_pagamento = forma_pagamento.id_forma_pagamento",
    }
    colunas = [
        "pessoa.nome AS nome_do_cliente",
        "pedido.id_pedido",
        "forma_pagamento.nome AS nome_forma_pagamento",
        "pedido.data_cadastro",
        "pedido.total",
        "pedido.numero_parcelas",
    ]
    filtros = {"pedido.id_func": None}  # Filtrar pedidos onde id_func é NULL
    if reverse:
        result = Busca_SQL_Join(
            base_table=base_table,
            join_conditions=join_conditions,
            colunas=colunas,
            not_filtros=filtros,
            order_by="pedido.data_cadastro",
        )
    else:
        result = Busca_SQL_Join(
            base_table=base_table,
            join_conditions=join_conditions,
            colunas=colunas,
            filtros=filtros,
            order_by="pedido.data_cadastro",
        )
    exibir_tabela(result, "Pedidos sem Baixa")
    return result


def Efetivar_Compra(id_f):
    result = Exibir_Compras_Efetivadas()
    id_pedido = int(input("Digite o ID do pedido que deseja dar baixa: "))
    if Verifica_ID("", [["id_pedido", id_pedido]], data=result):
        response = Altera_SQL(
            {"table": "pedido", "id_pedido": id_pedido, "id_func": id_f}, "id_pedido"
        )
        if Autentica_Dados(response):
            print("Baixa Concluida")
    else:
        print("ID Invalido")


def Exibir_Estoque():
    dados_estoque = Busca_SQL({"table": "estoque"}, filter_data=False)

    print("\nEstoque Atual:")
    if dados_estoque["result"] == []:
        print("Nenhum Produto Registrado no Estoque")
    else:
        estoque = dados_estoque["result"]
        tabela = PrettyTable()
        tabela.field_names = list(estoque[0].keys())
        for x in estoque:
            tabela.add_row(x.values())

        print(tabela)
        time.sleep(1)


def Adicionar_Produto():
    dados = ["camisa", "1", "camisa", "5", "vemelha", "2", "10"]
    # dados = Perguntas_Respostas(["Digite o nome do Produto", "Digite o Sexo Indicado para o produto:\n(1) - Feminino\n(2) - Masculino\n(3) - Unissex", "Digite a Categoria do Produto", "Digite o tamanho", "Digite a cor", "Digite a Quantidade", "Digite o preco"])
    dados = Cadastro_SQL(
        {
            "table": "estoque",
            "nome": dados[0],
            "sexo": dados[1],
            "categoria": dados[2],
            "tamanho": dados[3],
            "cor": dados[4],
            "quantidade": dados[5],
            "preco": dados[6],
        }
    )
    if Autentica_Dados(dados):
        Modifica_F_P_Produto(id_p=dados["last_id"], id_f_p=-1, acao=1)
        print("Estoque Cadastrado Com sucesso !")


def Remover_Produto():
    id_p = int(input("Defina o ID do produto que deseja Excluir:"))
    dados = Delete_SQL({"table": "estoque", "id_produto": id_p})
    if Autentica_Dados(dados):
        print("Produto Removido com Sucesso")


def Modificar_Estoque():
    id_p = int(input("Defina o ID do produto que deseja modificar:"))
    selecao = int(
        input(
            "Deseja modificar todos os campos do Produto ?:\n(1) - Sim\n(2) - Nao\nSua Escolha: "
        )
    )
    if selecao == 1:
        dados = Perguntas_Respostas(
            [
                "Digite o nome do Produto",
                "Digite o Sexo Indicado para o produto:\n(1) - Feminino\n(2) - Masculino\n(3) - Unissex",
                "Digite a Categoria do Produto",
                "Digite o tamanho",
                "Digite a cor",
                "Digite a Quantidade",
                "Digite o preco",
            ]
        )
        dados = {
            "table": "estoque",
            "id_produto": id_p,
            "nome": dados[0],
            "sexo": dados[1],
            "categoria": dados[2],
            "tamanho": dados[3],
            "cor": dados[4],
            "quantidade": dados[5],
            "preco": dados[6],
        }

    else:
        print(
            "Nome - 1\nSexo - 2\nCategoria - 3\nTamanho - 4\nCor - 5\nQuantidade - 6\nPreco - 7"
        )
        desc = int(input("Digite o campo que deseja Alterar: "))
        val = input("Digite o Valor desejado: ")
        dados = {
            "table": "estoque",
            "id_produto": id_p,
            ["", "Nome", "Sexo", "Categora", "Tamanho", "Cor", "Quantidade", "Preco"][
                desc
            ]: val,
        }

    dados = Altera_SQL(dados, "id_produto")
    if Autentica_Dados(dados):
        print("Linha Modificada com Sucesso")


def Menu_ADM(user):
    while True:
        print("=" * 30)
        print(" " * 10 + "ADM DA LOJA")
        print("=" * 30)
        print("Selecione uma opção (0/Sair): ")
        selecao = int(
            input(
                "(1) - Relatorio de Vendas\n(2) - Relatorio de Usuarios\n(3) - Relatorio de Estoque\n(4) - Relatorio de Funcionario\n(5) - Financeiro\n(6) - Cadastro de Funcionario\n(7) - Cadastro de Administrador\n(8) - Registros de Logs\n\nSua Escolha:"
            )
        )
        if selecao == 1:
            Relatorio_Vendas()
        elif selecao == 2:
            Relatorio_Usuarios()
            pass
        elif selecao == 3:
            Relatorio_Estoque()
            pass
        elif selecao == 4:
            escolha = int(
                input("Deseja Filtrar por data ?\n(1) - Sim\n(2) - Não\nSua Escolha: ")
            )
            i = None
            f = None
            if escolha == 1:
                i = input("Defina a Data de Inicio para Busca (0/Sem data inicio): ")
                i = i if i != 0 else None
                f = input("Defina a Data Final da Busca (0/Sem data Final): ")
                f = f if f != 0 else None

            Relatorio_Funcionario(data_inicio=i, data_fim=f)
        elif selecao == 5:
            Loja_Financeiro()
        elif selecao == 6:
            Cadastro(funcionario=True)
        elif selecao == 7:
            Cadastro(adm=True)
        elif selecao == 8:
            exibir_tabela(Busca_SQL({"table": "log_acoes"}, filter_data=False), "LOGS")
        elif selecao == 0:
            break


def Relatorio_Vendas():
    exibir_tabela(
        Busca_SQL({"table": "relatorio_vendas"}, filter_data=False),
        "Relatorio de Vendas",
    )


def exibir_tabela(dados, titulo, total=""):
    if dados["result"] is None or dados["result"] == []:
        print(f"Sem dados para {titulo}")
        time.sleep(1)
        return False

    dados = [
        {
            chave: (valor if valor not in [None, "None"] else "N/A")
            for chave, valor in item.items()
        }
        for item in dados["result"]
    ]
    tabela = PrettyTable()
    tabela.field_names = dados[0].keys()
    for item in dados:
        tabela.add_row(item.values())
    if total != "":
        if type(total[1]) == type(1):
            valor_total = sum([x[total[0]] * total[1] for x in dados])

        else:
            valor_total = sum([x[total[0]] * x[total[1]] for x in dados])
        matriz = [" -- " for x in range(len(dados[0].keys()))]
        matriz[0] = "Total"
        matriz[-1] = valor_total
        tabela.add_row(matriz)

    print(f"\n{'=' * 10}\n{titulo}:")
    print(tabela)
    time.sleep(1)
    return True


def Relatorio_Usuarios():
    exibir_tabela(
        Busca_SQL({"table": "relatorio_usuarios"}, filter_data=False),
        "Relatorio de Usuarios",
    )


def Relatorio_Funcionario(data_inicio, data_fim):
    base_table = "pedido"
    join_conditions = {"pessoa AS f": "pedido.id_func = f.id_pessoa"}
    colunas = [
        "f.id_pessoa AS id_funcionario",
        "f.nome AS nome_funcionario",
        "COUNT(pedido.id_pedido) AS total_pedidos",
        "SUM(pedido.total) AS total_dinheiro",
    ]
    filtros = {"f.tipo": "funcionario"}
    comparacoes = {}

    # Adicionar filtros de data, se fornecidos
    if data_inicio:
        comparacoes["pedido.data_cadastro"] = ">="
        filtros["pedido.data_cadastro >= "] = data_inicio
    if data_fim:
        comparacoes["pedido.data_cadastro"] = "<="
        filtros["pedido.data_cadastro <= "] = data_fim

    result = Busca_SQL_Join(
        base_table=base_table,
        join_conditions=join_conditions,
        colunas=colunas,
        filtros=filtros,
        comparacoes=comparacoes,
        group_by="f.id_pessoa, f.nome",
        order_by="total_pedidos DESC",
    )

    exibir_tabela(result, "Relatorio Funcionarios")


def Relatorio_Estoque():
    exibir_tabela(
        Busca_SQL({"table": "relatorio_estoque"}, filter_data=False),
        "Relatorio de Estoque",
    )


def Exibir_Formas_Pagamento():
    formas = Busca_SQL({"table": "forma_pagamento"}, filter_data=False)
    if Autentica_Dados(formas):
        if formas["result"] == [] or formas["result"] == None:
            print("Nenhuma Forma de Pagamento Cadastrada")
        else:
            tabela = PrettyTable()
            formas = formas["result"]
            formas = [
                {
                    chave: (
                        valor
                        if (chave == "permite_parcelamento" and valor == 0) == False
                        else "Não"
                    )
                    for chave, valor in dic.items()
                }
                for dic in formas
            ]
            formas = [
                {
                    chave: (
                        valor
                        if (chave == "permite_parcelamento" and valor == 1) == False
                        else "Sim"
                    )
                    for chave, valor in dic.items()
                }
                for dic in formas
            ]
            tabela.field_names = list(formas[0].keys())
            for x in formas:
                tabela.add_row(x.values())

            print(tabela)
            time.sleep(1)


def Adiciona_F_Pagamento():
    dados = Perguntas_Respostas(
        [
            "Digite o Nome da Forma de Pagamento",
            "É possivel Parcelar nessa forma ? (0/Não e 1/Sim)",
        ]
    )
    dados[1] = True if dados[1] == "1" else False
    response = Cadastro_SQL(
        {"table": "forma_pagamento", "nome": dados[0], "permite_parcelamento": dados[1]}
    )
    if Autentica_Dados(response):
        print("Forma de Pagamento Cadastrada com Sucesso")


def Remove_F_Pagamento():
    id_p = int(input("Defina o ID da forma de Pagamento que deseja Excluir:"))
    dados = Delete_SQL({"table": "forma_pagamento", "id_forma_pagamento": id_p})
    if Autentica_Dados(dados):
        print("Removido com Sucesso")


def Exibir_Produtos_Pagamento():
    dados = execute_query(
        """
                          SELECT 
    e.id_produto,
    e.nome AS nome_produto,
    e.preco,
    fp.id_forma_pagamento,
    fp.nome AS nome_forma_pagamento
FROM 
    estoque e
LEFT JOIN 
    produto_forma_pagamento pfp ON e.id_produto = pfp.id_produto
LEFT JOIN 
    forma_pagamento fp ON pfp.id_forma_pagamento = fp.id_forma_pagamento
ORDER BY 
    e.id_produto, 
    fp.id_forma_pagamento;""",
        directly=True,
    )
    if Autentica_Dados(dados):
        exibir_tabela(dados, "Produtos e Formas de Pagamento")


def Modifica_F_P_Produto(acao, id_p="", id_f_p=""):
    if id_p != "":
        id_produto = id_p
        id_forma_pag = id_f_p
    else:
        id_produto = int(input("Digite o Id do Produto (-1/Todos): "))
        Exibir_Formas_Pagamento()
        id_forma_pag = int(input("Defina o ID da forma de Pagamento (-1/Todas): "))

    if id_produto == -1 or id_forma_pag == -1:
        if id_produto == -1:
            dados = [
                {"table": "produto_forma_pagamento", "id_produto": x["id_produto"]}
                for x in Busca_SQL({"table": "estoque"}, filter_data=False)["result"]
            ]
        else:
            dados = [{"table": "produto_forma_pagamento", "id_produto": id_produto}]

        novos_dados = []
        if id_forma_pag == -1:
            formas_pagamento = Busca_SQL(
                {"table": "forma_pagamento"},
                colunas=["id_forma_pagamento"],
                filter_data=False,
            )["result"]
            for x in dados:
                for y in formas_pagamento:
                    x["id_forma_pagamento"] = y["id_forma_pagamento"]
                    novos_dados.append(copy.deepcopy(x))

            dados = novos_dados
        else:
            for x in dados:
                x["id_forma_pagamento"] = id_forma_pag
    else:
        dados = [
            {
                "table": "produto_forma_pagamento",
                "id_produto": id_produto,
                "id_forma_pagamento": id_forma_pag,
            }
        ]

    if acao == 1:
        for x in dados:
            Cadastro_SQL(x)
    elif acao == 0:
        for x in dados:
            Delete_SQL(x)
    print("Forma de Pagamento do Produto Alterada com Sucesso")


def Loja_Financeiro():
    print(f'{"="*50}\n{" "*10}Financeiro Loja de Roupas\n{"="*50}')

    while True:
        selecao = int(
            input(
                "Digite uma Opção (0/Sair):\n(1) - Formas de Pagamento\n(2) - Produtos e Formas de Pagamento\n\nSua Escolha: "
            )
        )
        if selecao == 1:
            while True:
                if Exibir_Formas_Pagamento():
                    selecao = int(
                        input(
                            "Digite uma Opção(0/ Sair):\n(1) -  Cadastrar Forma de Pagamento\n(2) - Remover Forma de Pagamento\n\nSua Escolha: "
                        )
                    )
                    if selecao == 0:
                        break
                    elif selecao == 1:
                        Adiciona_F_Pagamento()
                    elif selecao == 2:
                        Remove_F_Pagamento()
                else:
                    break
        elif selecao == 2:
            while True:
                Exibir_Produtos_Pagamento()

                selecao = int(
                    input(
                        "Oque Deseja Fazer (0/ Sair):\n(1) - Adicionar Forma de pagamento para Produto\n(2) - Remover forma de pagamento para Produto\n\nSua Escolha:"
                    )
                )
                if selecao == 0:
                    break
                elif selecao == 1:
                    Modifica_F_P_Produto(1)
                elif selecao == 2:
                    Modifica_F_P_Produto(0)

        elif selecao == 0:
            break
