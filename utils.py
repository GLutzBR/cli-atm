import os


def header():
    print("****************************************")
    print("*** School of Net - Caixa Eletrônico ***")
    print("****************************************")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
