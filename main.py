from console import CashMachineConsole, AuthBankAccountConsole
from utils import *


def main():
    clear_screen()
    header()

    if AuthBankAccountConsole.is_auth():
        clear_screen()
        header()
        CashMachineConsole.call_operation()
    else:
        print("Conta inválida")


if __name__ == '__main__':
    while True:
        main()

        input("Pressione <ENTER> para continuar...")
