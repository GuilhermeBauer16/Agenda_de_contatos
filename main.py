import mysql.connector
import functions
config = {

    'host': "127.0.0.1" ,
    'port': "3306" ,
    'user': "root" ,
    'password': "0910",
    'database': 'usuarios',
    'raise_on_warnings': True

}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
senha = ''

banco_usuarios = """CREATE DATABASE IF NOT EXISTS usuarios
                    DEFAULT CHARACTER SET "utf8'
                    DEFAULT COLLATE utf8_general_ci"""
def regista():
    global cursor
    global senha 
    nome = input('Digite seu nome: ')
    senha = input('Digite sua senha: ')
    try :
        dados = f'''CREATE DATABASE IF NOT EXISTS {nome.replace(' ','_')}
                DEFAULT CHARACTER SET "utf8'
                DEFAULT COLLATE utf8_general_ci'''
        cursor.execute(dados)
        cursor.execute(f'''INSERT INTO usuarios ''')
    except mysql.connector.Error as erro:
        print( f'erro {erro}')
        print('ouve um erro para registar o usuario ')



# user = input('Digite o nome do usuario: ').upper()
# password = input('Digite sua senha: ')
# print('Agenda de contatos ')

while True:
    functions.titulo('Login')
    print("""

[1]Registar usuario 
[2]Login
[3]Sair 
""")
    print('==' * 50)
    opcao = functions.converson_numero('Sua opção: ', int )
    print('==' * 50)

    if opcao == 1: 
        regista()

#fecha o banco de dados 
connection.close()
cursor.close()