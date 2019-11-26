import getpass
from auth import AuthBankAccount
from cash_machine import CashMachineWithdraw, CashMachineInsertMoneyBill, CashMachineGetter


class AuthBankAccountConsole:

    @staticmethod
    def is_auth():
        account_number_typed = input("Digite sua conta: ")
        password_typed = getpass.getpass("Digite sua senha: ")

        return AuthBankAccount.authenticate(account_number_typed, password_typed)


class CashMachineConsole:

    @staticmethod
    def call_operation():
        CashMachineOperation.do_operation(CashMachineConsole.__get_menu_options_typed())

    @staticmethod
    def __get_menu_options_typed():
        print(f"{CashMachineOperation.OPERATION_SHOW_BALANCE} - Saldo")
        print(f"{CashMachineOperation.OPERATION_WITHDRAW} - Saque")
        bank_account = AuthBankAccount.bank_account_authenticated
        if bank_account.admin:
            print(f"{CashMachineOperation.OPERATION_BANKNOTE_EXTRACT} - Extrato de notas no caixa eletrônico")
            print(f"{CashMachineOperation.OPERATION_INSERT_MONEY_SLIPS} - Incluir cédulas")
            print(f"{CashMachineOperation.OPERATION_TURNOFF_ATM} - Desligar caixa eletrônico")

        return input("Escolha uma das opções acima: ")


class CashMachineOperation:
    OPERATION_SHOW_BALANCE = '1'
    OPERATION_WITHDRAW = '2'
    OPERATION_BANKNOTE_EXTRACT = '9'
    OPERATION_INSERT_MONEY_SLIPS = '10'
    OPERATION_TURNOFF_ATM = '11'

    @staticmethod
    def do_operation(option):
        bank_account = AuthBankAccount.bank_account_authenticated
        if option == CashMachineOperation.OPERATION_SHOW_BALANCE:
            ShowBalanceOperation.do_operation()
        elif option == CashMachineOperation.OPERATION_WITHDRAW:
            WithdrawOperation.do_operation()
        elif option == CashMachineOperation.OPERATION_INSERT_MONEY_SLIPS and bank_account.admin:
            InsertMoneyBillOperation.do_operation()
        elif option == CashMachineOperation.OPERATION_TURNOFF_ATM and bank_account.admin:
            ShutDownCashMachineOperation.do_operation()
        elif option == CashMachineOperation.OPERATION_BANKNOTE_EXTRACT and bank_account.admin:
            PrintMoneySlipsOperation.do_operation()


class ShowBalanceOperation:
    @staticmethod
    def do_operation():
        bank_account = AuthBankAccount.bank_account_authenticated
        print(f"Seu saldo é de R$ {bank_account.value:.2f}")


class WithdrawOperation:
    @staticmethod
    def do_operation():
        value_typed = int(input("Digite o valor a ser sacado: "))
        bank_account = AuthBankAccount.bank_account_authenticated
        cash_machine, account_balance_availability = CashMachineWithdraw.withdraw(bank_account, value_typed)
        if cash_machine.value_remaining != 0:
            print("O caixa não possui cédulas disponíveis para este valor")
        elif not account_balance_availability:
            print("Valor indisponível para saque, consulte seu saldo!")
        else:
            print("Pode retirar as seguintes notas:")
            print(cash_machine.money_slips_user)
            print(f"\nSeu saldo agora é de R$ {bank_account.value:.2f}\n")


class InsertMoneyBillOperation:

    @staticmethod
    def do_operation():
        amount_typed = int(input('Digite a quantidade de cédulas: '))
        money_bill_typed = int(input("Digite a cédula a ser incluída: "))

        cash_machine = CashMachineInsertMoneyBill.insert_money_bill(money_bill_typed, amount_typed)
        print(cash_machine.money_slips)


class PrintMoneySlipsOperation:

    @staticmethod
    def do_operation():
        print(CashMachineGetter().get().money_slips)


class ShutDownCashMachineOperation:

    @staticmethod
    def do_operation():
        exit()
