import mysql.connector
import functions
from time import sleep

config = {

    'host': "localhost" ,
    'port': "3306" ,
    'user': "root" ,
    'password': "0910",
    'raise_on_warnings': True

}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
senha = ''
nome = ''

def registra():
    # global nome
    # global senha 
    nome = str(input('Digite seu nome: '))
    senha = str(input('Digite sua senha: '))
    banco = [nome , ]

    try :
        dados = f'''CREATE DATABASE IF NOT EXISTS {nome.replace(' ','_')}
                DEFAULT CHARACTER SET 'utf8mb4'
                DEFAULT COLLATE utf8mb4_general_ci'''
        cursor.execute(dados)
        cursor.execute(f'''
                       CREATE USER "{nome.replace(' ', '_')}"@"localhost" 
                       IDENTIFIED BY "{connection.converter.escape(senha)}"''')  
        cursor.execute(f"""
                       GRANT ALL PRIVILEGES ON {nome.replace(' ','_')}.*
                        TO '{nome.replace(' ','_')}'@'localhost' """)
        connection.commit()
        connection.close()
        cursor.close()
    except mysql.connector.Error as erro:
        print( f'erro {erro}')
        print('ouve um erro para registar o usuario ')


def login():

    nome = str(input('Digite seu nome: '))
    senha = str(input('Digite sua senha: '))

    try: 
        
        cursor.execute(f'''USE {nome.replace(' ', '_')}''')
        cursor.execute(f'''SELECT COUNT(*) FROM mysql.user WHERE user = "{nome.replace(' ', '_')}"
                       AND authentication_string = "{senha}"''')
        result = cursor.fetchone()

        if result[0] == 1:
            print(f'Login bem sucedido, seja bem vindo {nome.replace('_', ' ')}')
        
        else:
            print('\033[31mUsuario ou senha incorretos\033[m')

    except mysql.connector.Error as erro:
        print(f'ocorreu o erro{erro}')


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
        registra()

    elif opcao == 2:
        login()
    
    elif opcao == 3:
        print('saindo...')
        sleep(1)
        functions.limpa_terminal()
        break

#fecha o banco de dados 
connection.close()
cursor.close()