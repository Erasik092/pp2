import csv
from connect import get_connection

def insert_from_csv(file_path):
    conn = get_connection()
    if conn is None: return
    
    cursor = conn.cursor()
    
    with open(file_path, mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            # row[0] это имя, row[1] это телефон
            name = row[0]
            phone = row[1]
            
            try:
                cursor.execute(
                    "INSERT INTO PhoneBook (user_name, phone_number) VALUES (%s, %s)",
                    (name, phone)
                )
                print(f"Добавлен контакт: {name}")
            except Exception as e:
                print(f"Ошибка при вставке {name}: {e}")
                conn.rollback() # Отмена, если что-то пошло не так
    
    conn.commit() # Сохраняем всё в базе
    cursor.close()
    conn.close()

def update_contact(name, new_phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE PhoneBook SET phone_number = %s WHERE user_name = %s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()

# Запускаем функцию
if __name__ == "__main__":
    insert_from_csv('contacts.csv')