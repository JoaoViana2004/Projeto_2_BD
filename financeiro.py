from connect import *
from loja import *

dados_user = Login(id_u=3)
Menu_ADM(dados_user)

# Menu_ADM(Login(id_u=1))


# import datetime


# def Ajeita_Data(data_atual):
#     return "{}/{}/{}".format(data_atual.day, data_atual.month, data_atual.year)


# data = datetime.date.today()

# print(Ajeita_Data(data))

# data = data + datetime.timedelta(days=120)

# print(Ajeita_Data(data))
