class Clients:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def add_money(self, summa):
        self.balance = self.balance + summa

    def buy(self, price):
        if price <= self.balance:
            self.balance = self.balance - price
            print(f'Вы совершили покупку на сумму {price} руб.')
        else:
            print(f'У вас не достаточно средст. Вам необходимо пополнить кошелек на {price-self.balance}')

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def print_money_status(self):
        print(f'Клиент "{self.name}". Баланс: {self.balance} руб.')


class Guest(Clients):
    def __init__(self, name='', city='', status='', balance=0):
        super().__init__(name, balance)
        self.city = city
        self.status = status

    def init_from_dict(self, guest_list):
        self.name = guest_list.get('name')
        self.city = guest_list.get('city')
        self.balance = guest_list.get('balance')
        self.status = guest_list.get('status')

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_city(self, city):
        self.city = city

    def get_city(self):
        return self.city



