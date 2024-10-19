from loja import *
from connect import *

err = 0

while True:
    user = Menu_Usuario()
    if user != None:
        if user["tipo"] == "adm":
            Menu_ADM()
        elif user["tipo"] == "funcionario":
            Menu_Funcionario(user)
        else:
            user = Menu_Usuario(id_u=user["id_pessoa"])
