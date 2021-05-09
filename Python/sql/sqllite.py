import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE people (
            id integer,
            name text,
            last text
            )""")


class people:
    def __init__(self, uid, name, last):
        self.id = uid
        self.name = name
        self.last = last

    @property
    def full(self):
        return f"{self.name} {self.last}"

    @property
    def email(self):
        return f"{self.name}_{self.last}{self.id}@email.com"

    def __repr__(self):
        return f"people({self.id}, '{self.name}', '{self.last}')"


def insert_user(user):
    with conn:
        c.execute("INSERT INTO people VALUES (:id, :name, :last)", {'id': user.id, 'name': user.name, 'last': user.last})


def get_user_by_name(last):
    c.execute("SELECT * FROM people WHERE last=:last", {'last': last})
    return c.fetchall()


def update_id(user, uid):
    with conn:
        c.execute("""UPDATE people SET id = :id
                    WHERE name = :name AND last = :last""", {'id': uid, 'name': user.name, 'last': user.last})


def remove_user(user):
    with conn:
        c.execute("DELETE from people WHERE name = :name AND last = :last",
                  {'name': user.name, 'last': user.last})


emp_1 = people(9, 'John', 'Doe')
emp_2 = people(8, 'Jane', 'Doe')

insert_user(emp_1)
insert_user(emp_2)

emps = get_user_by_name('Doe')
print(emps)

update_id(emp_2, 95000)
remove_user(emp_1)

emps = get_user_by_name('Doe')
print(emps)

i = input(">")
