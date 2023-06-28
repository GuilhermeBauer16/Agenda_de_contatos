import mysql.connector
import functions
from time import sleep

config = {

    'host': "localhost" ,
    'port': "3306" ,
    'user': "root" ,
    'password':"0910" ,
    'raise_on_warnings': True

}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

def registra():

    global cursor
    global connection 
    sleep(1)
    functions.limpa_terminal()
    functions.titulo('Novo usuário')
    nome = str(input('Digite seu nome: '))
    senha = str(input('Digite sua senha: '))

    try :

        dados = f'''CREATE DATABASE IF NOT EXISTS {nome.replace(' ','_')}
                DEFAULT CHARACTER SET 'utf8mb4'
                DEFAULT COLLATE utf8mb4_general_ci'''
        
        cursor.execute(dados)
        cursor.execute(f'''
                       CREATE USER "{nome.replace(' ', '_')}"@"localhost" 
                       IDENTIFIED BY "{senha}"''')  
        cursor.execute(f"""
                       GRANT ALL PRIVILEGES ON {nome.replace(' ','_')}.*
                        TO '{nome.replace(' ','_')}'@'localhost' """)
        connection.commit()
        print(f'\033[32mNovo usuário {nome.replace('_', ' ')} cadastrado com sucesso\033[m')
        sleep(1)
        functions.limpa_terminal()

    except mysql.connector.Error as erro:
        print('ouve um erro para registar o usuario ')


while True:
    functions.titulo('Agenda de contatos')
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
        sleep(1)
        functions.limpa_terminal()
        while True:
            functions.titulo('Login')
            nome = str(input('Digite seu nome: '))
            senha = str(input('Digite sua senha: '))

            try: 
                config = {f'''

            'host': "localhost" ,
            'port': "3306" ,
            'user': "{nome}" ,
            'password': "{senha}",
            'raise_on_warnings': True
                '''}
                cursor.execute(f"SHOW GRANTS FOR '{nome.replace(' ','_')}'@'localhost'")
                resulta = cursor.fetchall()
                print(f'\033[32mLogin do usuário {nome.replace('_', ' ')} realizado com sucesso\033[m')
                sleep(1)
                functions.limpa_terminal()
                break

            except mysql.connector.Error as erro:
                print('\033[31mUsuario ou senha incorretos\033[m')

        while True:
            functions.titulo("Funções")
            print('''
    [1]Novo Contato
    [2]Editar Contato
    [3]Deletar Contato
    [4]Filtrar por Contato
    [5]Voltar ao menu de login 
                ''')
            
            print('==' * 50)
            opcao_contato = functions.converson_numero('Sua opção: ', int)
            cursor.execute(f'''USE {nome.replace(' ', '_')}''')
            sleep(1)
            functions.limpa_terminal()
            if opcao_contato == 1:
                functions.titulo("Novo contato ")
                nome_contato = str(input('Nome: '))
                telefone = str(input('Telefone: '))
                email = str(input('email: '))
                
                try: 
                    table =  f"""CREATE TABLE IF NOT EXISTS {nome_contato.replace(' ','_')}(
                                id INT NOT NULL AUTO_INCREMENT ,
                                nome VARCHAR(150) NOT NULL,
                                telefone VARCHAR(15) NOT NULL , 
                                email VARCHAR(150),
                                PRIMARY KEY(id))
                                default charset = utf8mb4"""

                    cursor.execute(table)

                    inserir = f'''INSERT INTO {nome_contato.replace(' ','_')}
                    (nome , telefone , email ) VALUES 
                    (%s , %s , %s )'''
                    valores = ( nome_contato , telefone.replace(' ','_') , email)

                    cursor.execute(inserir,valores)
                    connection.commit()
                    print(f"\033[32m{nome_contato.replace('_',' ')} adicionado com sucesso\033[m")
                    sleep(1.5)
                    functions.limpa_terminal()

                except mysql.connector.Error as erro:
                    print('\033[31mErro ao adicionar o contato ou o contato já existe\033[m')

            elif opcao_contato == 2:
                functions.titulo('Edição de contato')
                edita_contato = str(input('Digite o nome do contato que deseja editar: '))

                print('==' * 50)

                try:
                    cursor.execute(f"SHOW TABLES LIKE '{edita_contato.replace(' ','_')}'")
                    edita = cursor.fetchone()
                    if edita :
                        novo_nome_contato = str(input('Nome: '))
                        novo_telefone = str(input('Telefone: '))
                        novo_email = str(input('email: '))

                        update = f"""UPDATE {edita_contato.replace(' ','_')} SET
                        nome = %s , telefone = %s , email = %s """
                        novos_valores = (novo_nome_contato.replace(' ','_') , novo_telefone.replace(' ','_') , novo_email)
                        cursor.execute(update, novos_valores)
                        cursor.execute(f"""ALTER TABLE {edita_contato.replace(' ','_')}
                                       RENAME TO {novo_nome_contato.replace(' ','_')}""")
                        connection.commit()
                        print(f"\033[32mContato {novo_nome_contato.replace('_',' ')} editado com sucesso\033[m")                
                        sleep(1)
                        functions.limpa_terminal()
                
                except mysql.connector.Error as erro:
                    print('\033[31mErro ao editar o contato ou o contato não existe \033[m') 

            elif opcao_contato == 3:
                functions.titulo('Deleção do contato')
                nome_deletar = str(input('Digite o nome do contato que deseja deletar: '))
                print('==' * 50)

                try:
                    deleta = f"""DROP TABLE {nome_deletar.replace(' ','_')}"""
                    cursor.execute(deleta)
                    print(f"\033[32m{nome_deletar.replace('_',' ')} deletado com sucesso\033[m")
                    sleep(1.5)
                    functions.limpa_terminal()

                except mysql.connector.Error as erro:
                    print('\033[31mErro ao deletar o contato ou o contato não existe \033[m') 

            elif opcao_contato == 4:
                
                functions.titulo('Filtro')
                nome_filtrar = str(input('Digite o nome do contato que deseja filtrar: '))

                try:
                    filtro = f'''SELECT * FROM {nome_filtrar.replace(' ','_')}'''
                    cursor.execute(filtro)
                    tabela = cursor.fetchall()
                    if tabela:
                        for coluna in tabela:
                            functions.titulo('Contato')
                            print(f'Nome: {coluna[1]}')
                            print(f'telefone: {coluna[2].replace('_', ' ')}')
                            print(f'email: {coluna[3]}')

                except mysql.connector.Error as erro:
                    print('\033[31mErro ao deletar o contato ou o contato não existe \033[m')

            elif opcao_contato == 5:
                functions.titulo('Voltando ao menu de login ')
                sleep(1.5)
                functions.limpa_terminal()
                break

    elif opcao == 3:
        print('saindo...')
        sleep(1)
        functions.limpa_terminal()
        break

#fecha o banco de dados 
connection.close()
cursor.close()