from connect import get_connection

# 1. Вызов функции поиска
def search_contacts(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

# 2. Вызов процедуры Upsert
def add_or_update(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print(f"Upsert done for {name}")
    cur.close()
    conn.close()

# 3. Вставка списка (Массивы в Python -> Массивы в Postgres)
def add_many(names_list, phones_list):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_many_contacts(%s, %s)", (names_list, phones_list))
    conn.commit()
    cur.close()
    conn.close()

# 4. Пагинация
def get_page(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paged(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

# 5. Удаление
def remove_contact(identifier):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact_adv(%s)", (identifier,))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Примеры вызова:
    # add_or_update('Ivan', '87009998877')
    # add_many(['Alisa', 'Bob'], ['8777111', '123']) # '123' не пройдет валидацию length >= 5
    # search_contacts('Ivan')
    # get_page(5, 0)
    pass