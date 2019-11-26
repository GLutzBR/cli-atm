import os
import ast


class BankFile:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self. _file = None

    def _open_file_bank(self, mode):
        return open(self.BASE_PATH + '/_bank_file.dat', mode)

    def _read_lines(self):
        self._file = self._open_file_bank('r')
        lines = self._file.readlines()
        self._file.close()
        return lines

    def _write_lines(self, lines):
        self._file = self._open_file_bank('w')
        self._file.writelines(lines)
        self._file.close()


class BankAccountFile(BankFile):
    ACCOUNTS_LINE = 1


class BankAccountFileReader(BankAccountFile):

    def get_line_index_of_bank_account(self, account_number):
        lines = self._read_lines()
        lines = self.__skip_first_line(lines)
        line_index = -1
        for index, line in enumerate(lines):
            bank_account_created = self.__create_bank_account_from_file_line(line)
            if bank_account_created.check_account_number(account_number):
                line_index = index
                break
        return line_index + self.ACCOUNTS_LINE

    def get_account(self, account_number):
        lines = self._read_lines()
        lines = self.__skip_first_line(lines)
        bank_account = None
        for line in lines:
            bank_account_created = self.__create_bank_account_from_file_line(line)
            if bank_account_created.check_account_number(account_number):
                bank_account = bank_account_created
                break
        return bank_account

    def __create_bank_account_from_file_line(self, line):
        account_data = line.split(';')
        from cash_machine import BankAccount
        return BankAccount(
            account_data[0],
            account_data[1],
            account_data[2],
            float(account_data[3]),
            ast.literal_eval(account_data[4]),
        )

    def __skip_first_line(self, lines):
        return lines[self.ACCOUNTS_LINE:len(lines)]


class BankAccountFileWriter(BankAccountFile):

    def write_bank_account(self, bank_account):
        line_index_to_update = BankAccountFileReader().get_line_index_of_bank_account(bank_account.account_number)
        lines = self._read_lines()
        lines[line_index_to_update] = self.__format_line_to_write(bank_account)
        self._write_lines(lines)

    def __format_line_to_write(self, bank_account):
        line = f"{bank_account.account_number};{bank_account.name};{bank_account.password};{bank_account.value};" \
               f"{bank_account.admin};"
        return line + '\n'


class MoneySlipsFile(BankFile):
    MONEY_SLIPS_LINE = 0


class MoneySlipsFileReader(MoneySlipsFile):

    def __init__(self):
        super().__init__()
        self.__money_slips = {}

    def get_money_slips(self):
        self._file = self._open_file_bank('r')
        line_to_read = self.MONEY_SLIPS_LINE
        line = self._file.readlines(line_to_read)[0]
        while self.__has_semicolon(line):
            semicolon_pos = line.find(';')
            money_bill_value = line[0:semicolon_pos]
            self.__add_money_slips_from_line(money_bill_value)
            if self.__last_money_bill(semicolon_pos, line):
                break
            else:
                line = line[semicolon_pos + 1:len(line)]
        return self.__money_slips

    def __last_money_bill(self, semicolon_pos, line):
        return semicolon_pos + 1 == len(line)

    def __has_semicolon(self, line):
        return line.find(';') != -1

    def __add_money_slips_from_line(self, money_bill_value):
        equal_pos = money_bill_value.find('=')
        money_bill = money_bill_value[0:equal_pos]
        value = money_bill_value[equal_pos + 1:len(money_bill_value)]
        self.__money_slips[int(money_bill)] = int(value)


class MoneySlipsFileWriter(MoneySlipsFile):

    def write_money_slips(self, money_slips):
        lines = self._read_lines()
        line_to_write = self.MONEY_SLIPS_LINE
        lines[line_to_write] = self.__format_line_to_write(money_slips)
        self._write_lines(lines)

    def __format_line_to_write(self, money_slips):
        line = ""
        for money_bill, value in money_slips.items():
            line += str(money_bill) + '=' + str(value) + ';'
        return line + '\n'
