import sqlite3

db = sqlite3.connect('Account.db')
cur = db.cursor()
    # Создаем таблицу
cur.execute("""CREATE TABLE IF NOT EXISTS Account (
    ID INTEGER PRIMARY KEY,
    PHONE TEXT,
    PASS TEXT,
    API_ID TEXT,
    API_HASH TEXT,
    ACTIVITY TEXT,
    LITECOIN TEXT
)""")

db.commit()

Phone = "+380661054982"
password = "13236546460"
Api_id = "1634158"
Api_hash = "1ea650a5f73b4074a90f8e2a086d2641"
Activity = "ON"
Litecoin = "ltc1qlhs4e459wwtu8sx7a4rtumtffs9lr4ktmfl6ny"

cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{Phone}'")
if cur.fetchone() is None:
    cur.execute("""INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY, LITECOIN) VALUES (?,?,?,?,?,?);""", (Phone, password, Api_id, Api_hash, Activity, Litecoin))
    db.commit()
    print("Зарегистрированно!")
    for value in cur.execute("SELECT * FROM Account"):
        print(value)