from file import BankAccountFileWriter


class BankAccount:

    def __init__(self, account_number, name, password, value, admin):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.value = value
        self.admin = admin

    def check_account_number(self, account_number):
        return account_number == self.account_number

    def check_password(self, password):
        return password == self.password

    def balance_debit(self, value):
        self.value -= value

    def __check_availability_to_withdraw(self, value):
        if self.value < value:
            return False
        return True


class CashMachineInsertMoneyBill:

    @staticmethod
    def insert_money_bill(money_bill, amount):
        cash_machine = CashMachineGetter().get()
        if money_bill not in cash_machine.money_slips.keys():
            cash_machine.money_slips[money_bill] = 0
        cash_machine.money_slips[money_bill] += amount
        from file import MoneySlipsFileWriter
        MoneySlipsFileWriter().write_money_slips(cash_machine.money_slips)
        return cash_machine


class CashMachineWithdraw:

    @staticmethod
    def withdraw(bank_account, value):
        account_balance_availability = CashMachineWithdraw.__check_availability_to_withdraw(bank_account, value)
        cash_machine = CashMachineGetter().get()
        money_slips_user = cash_machine.withdraw(value)
        if money_slips_user and account_balance_availability:
            CashMachineWithdraw.__balance_debit(bank_account, value)
            from file import MoneySlipsFileWriter
            MoneySlipsFileWriter().write_money_slips(cash_machine.money_slips)
        return cash_machine, account_balance_availability

    @staticmethod
    def __check_availability_to_withdraw(bank_account, value):
        if bank_account.value < value:
            return False
        return True

    @staticmethod
    def __balance_debit(bank_account, value):
        bank_account.balance_debit(value)
        BankAccountFileWriter().write_bank_account(bank_account)


class CashMachineGetter:

    def get(self):
        from file import MoneySlipsFileReader
        money_slips = MoneySlipsFileReader().get_money_slips()
        return CashMachine(money_slips)


class CashMachine:

    def __init__(self, money_slips):
        self.money_slips = money_slips
        self.money_slips_user = {}
        self.value_remaining = 0
        self.sorted_money_slips = {}

    def withdraw(self, value):
        self.value_remaining = value

        self.__calculate_money_slips_user()

        if self.value_remaining == 0:
            self.__decrease_money_slips()

        return False if self.value_remaining != 0 else self.money_slips

    def __calculate_money_slips_user(self):
        self.__sort_money_slips()

        for money_bill in self.sorted_money_slips.keys():
            if self.sorted_money_slips[money_bill] >= self.value_remaining // money_bill > 0:
                self.money_slips_user[money_bill] = self.value_remaining // money_bill
                self.value_remaining -= self.money_slips_user[money_bill] * money_bill

    def __sort_money_slips(self):
        for elements in sorted(self.money_slips.items(), reverse=True):
            self.sorted_money_slips[elements[0]] = elements[1]

    def __decrease_money_slips(self):
        for money_bill in self.money_slips_user:
            self.money_slips[money_bill] -= self.money_slips_user[money_bill]
