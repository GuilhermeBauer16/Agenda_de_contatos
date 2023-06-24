def converson_numero(msg,tipo= int):
    while True:
        numero = input(msg)

        try:
            num_convertido = tipo(numero) 
            break

        except ValueError:
            print('\033[31mPor favor digite um número\033[m')
    
    return num_convertido

def titulo(msg, num=50):
    quant = num * 2
    print('==' * num)
    print(f'{msg:^{quant}}')
    print('=='* num)


def limpa_terminal():
    import os 

    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

    