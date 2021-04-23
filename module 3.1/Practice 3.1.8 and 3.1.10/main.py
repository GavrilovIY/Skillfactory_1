from Pets import Cats
from clients import Clients, Guest

if __name__ == '__main__':
    baron = Cats(name="Baron", sex='Male', age=2)
    sem = Cats(name="Sem", sex='Male', age=2)

    ivan_petrov = Clients(name="Иван Петров")
    ivan_petrov.add_money(100)
    ivan_petrov.print_money_status()
    ivan_petrov = Guest(ivan_petrov.get_name(), city='Вологда', status='Волонтер', balance=ivan_petrov.get_balance())

    invite_list = [ivan_petrov]

    list_of_people = [
        {'name': "Сидр Сидоров", 'city': "Новосибирск", 'status': "Волонтер", 'balance': 0},
        {'name': "Петр Иванов", 'city': "Красноярск", 'status': "Организатор", 'balance': 0},
        {'name': "Никола Астровский", 'city': "Краснодар", 'status': "Помошник", 'balance': 0}]

    for person in list_of_people:
        guest = Guest()
        guest.init_from_dict(person)
        invite_list.append(guest)

    for guest in invite_list:
        guest.print_money_status()
