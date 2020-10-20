import sqlite3

# EXAMPLE Of Many-to-Many Database

class DatabaseContextManager(object):
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

def create_table_customer():
    query = """CREATE TABLE IF NOT EXISTS Customer(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                amount_spent FLOAT                
                )"""
    with DatabaseContextManager("orders") as orders:
        orders.execute(query)

def create_table_product():
    query = """CREATE TABLE IF NOT EXISTS Product(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price FLOAT,                
                description TEXT                
                )"""
    with DatabaseContextManager("orders") as orders:
        orders.execute(query)

def create_table_order():
    query = """CREATE TABLE IF NOT EXISTS Orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                FOREIGN KEY(customer_id) REFERENCES Customer(id),
                FOREIGN KEY(product_id) REFERENCES Product(id)                
                )"""
    with DatabaseContextManager("orders") as orders:
        orders.execute(query)

# ------------------------Customer CRUD------------------------
def create_customer(first_name: str, last_name: str, amount_spent: int):
    query = """INSERT INTO Customer(first_name, last_name, amount_spent) VALUES(?,?,?)"""
    parameters = [first_name, last_name, amount_spent]
    with DatabaseContextManager("orders") as orders:
        orders.execute(query, parameters)

# Read function
def get_customer():
    query = """SELECT * FROM Customer"""
    with DatabaseContextManager("orders") as orders:
        orders.execute(query)
        for record in orders.fetchall():
            print(record)
    print("------------------------------------------------------")

# ------------------------Product CRUD------------------------
def create_product(name: str, price: int, description: str):
    query = """INSERT INTO Product(name, price, description) VALUES(?,?,?)"""
    parameters = [name, price, description]
    with DatabaseContextManager("orders") as orders:
        orders.execute(query, parameters)

# Read function
def get_product():
    query = """SELECT * FROM Product"""
    with DatabaseContextManager("orders") as orders:
        orders.execute(query)
        for record in orders.fetchall():
            print(record)
    print("------------------------------------------------------")

# ------------------------Orders CRUD------------------------
def create_order(customer_id: int, product_id: int):
    query = """INSERT INTO Orders(customer_id, product_id) VALUES(?,?)"""
    parameters = [customer_id, product_id]
    with DatabaseContextManager("orders") as orders:
        orders.execute(query, parameters)

# Read function
def get_order():
    query = """SELECT * FROM Orders"""
    with DatabaseContextManager("orders") as orders:
        orders.execute(query)
        for record in orders.fetchall():
            print(record)
    print("------------------------------------------------------")


def get_customer_orders():
    query = """SELECT Customer.first_name, Customer.last_name, Product.name, Product.description  FROM Orders
                JOIN Customer
                    ON Customer.id = Orders.customer_id
                JOIN Product
                    ON Product.id = Orders.product_id    
                    """
    with DatabaseContextManager("orders") as orders:
        orders.execute(query)
        for row in orders.fetchall():
            print(row)

create_table_customer()
create_table_product()
create_table_order()

create_customer ("jonas", "jonaitis", 10)
create_customer ("petras", "petraitis", 20)

create_product("knyga", 5, "fantastika")
create_product("knyga", 5, "detektyvas")
create_product("knyga", 5, "dokumentika")

create_order(1, 1)
create_order(1, 2)
create_order(2, 3)

get_customer_orders()