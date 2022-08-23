
import psycopg2

# Функция, создающая структуру БД (таблицы)
def create_table (table_name):
   # cur.execute(f"""
   # DROP TABLE {table_name};
   # """)
   cur.execute(f"""
   CREATE TABLE IF NOT EXISTS {table_name}
   (
   id SERIAL PRIMARY KEY,
   First_name VARCHAR(40) NOT NULL,
   Second_name VARCHAR(60) NOT NULL,
   Email VARCHAR(60) UNIQUE
  ) ;
   """)
   conn.commit()

# Функция, позволяющая добавить нового клиента
def add_client(table_name, first_name1, second_name1, email1):
  cur.execute(f"""
       INSERT INTO {table_name}(First_name, Second_name, Email) values (%s, %s, %s);
  """, (first_name1, second_name1, email1))
  conn.commit()

# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(table_name, client_id, phone):
   # cur.execute(f"""
   # DROP TABLE Phones;
   # """)
   cur.execute(f"""
   CREATE TABLE IF NOT EXISTS Phones
   (
   id SERIAL PRIMARY KEY,
   Phone VARCHAR(30) UNIQUE,
   client_id INTEGER NOT NULL REFERENCES {table_name}(id)
   );
   """)
   cur.execute(f"""
   INSERT INTO Phones(Phone, client_id) values (%s, %s);
   """, (phone, client_id))
   conn.commit()

# Функция, позволяющая изменить данные о клиенте
def change_client(table_name, client_id, first_name=None, second_name=None, email=None, phone=None, phone_old=None):
   cur.execute(f"""
       UPDATE {table_name} SET First_name = %s WHERE id = %s AND %s != 'None';
       """, (first_name, client_id, first_name))
   cur.execute(f"""
       UPDATE {table_name} SET First_name = %s WHERE id = %s AND %s != 'None';
       """, (second_name, client_id, second_name))
   cur.execute(f"""
       UPDATE {table_name} SET First_name = %s WHERE id = %s AND %s != 'None';
       """, (email, client_id, email))
   if phone_old == None:
     cur.execute(f"""
       UPDATE Phones
       SET Phone = '{phone}'
       WHERE client_id = %s;
     """, (client_id,))
   else:
       cur.execute(f"""
         UPDATE Phones
         SET Phone = '{phone}'
         WHERE client_id = %s AND phone = %s;
       """, (client_id, phone_old))
   conn.commit()

# Функция, позволяющая удалить телефон для существующего клиента
def del_phone(client_id, phone):
    cur.execute(f"""
     DELETE FROM Phones WHERE client_id = %s AND phone = %s;
    """, (client_id, phone))
    conn.commit()

# Функция, позволяющая удалить существующего клиента
def del_client(table_name, client_id):
    cur.execute(f"""
    DELETE FROM Phones WHERE client_id = %s;
    """, (client_id,))
    cur.execute(f"""
    DELETE FROM {table_name} WHERE id = %s;  
    """, (client_id,))
    conn.commit()

# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(table_name, first_name=None, second_name=None, email=None, phone=None):
    cur.execute(f"""
    SELECT id FROM {table_name} WHERE First_name = %s;
    """, (first_name,))
    print(cur.fetchall())
    cur.execute(f"""
    SELECT id FROM {table_name} WHERE Second_name = %s;
    """, (second_name,))
    print(cur.fetchall())
    cur.execute(f"""
    SELECT id FROM {table_name} WHERE Email = %s;
    """, (email,))
    print(cur.fetchall())
    cur.execute(f"""
    SELECT client_id FROM Phones WHERE phone = %s;
    """, (phone,))
    print(cur.fetchall())

if __name__ == '__main__':

    with psycopg2.connect(database="clients_db", user="postgres", password="0000") as conn:
        with conn.cursor() as cur:
            create_table("clients")
            add_client("clients", "Sergey", "Morozov", "email5@mail.ru")
            add_client("clients", "Igor", "Novik", "emailnov@mail.ru")
            add_client("clients", "Vasiliy", "Starostin", "star@mail.ru")
            add_phone("clients", "1", "89090251254")
            add_phone("clients", "1", "89090200000")
            add_phone("clients", "2", "89091111111")
            change_client("clients", "2", first_name="Pavel", phone="9999999999")
            change_client("clients", "1", first_name="Alexander", second_name="Akulov", email="@@@@", phone="856444444445", phone_old="89090251254")
            del_phone(1, '856444444445')
            del_client("clients", 1)
            add_client("clients", "Sergey", "Morozov", "eil5@mail.ru")
            find_client("clients", first_name="Sergey")
            find_client("clients", second_name="Novik")
            find_client("clients", email="star@mail.ru")
            find_client("clients", phone="9999999999")
    conn.close()
