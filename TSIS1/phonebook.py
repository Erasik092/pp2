import json
import csv
from connect import get_conn

# ---------------- HELPERS ----------------

def fetch(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or ())
    data = cur.fetchall()
    conn.close()
    return data


def execute(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    conn.close()


# ---------------- SEARCH / FILTER ----------------

def search_contacts():
    q = input("Search query: ")
    rows = fetch("SELECT * FROM search_contacts(%s)", (q,))
    for r in rows:
        print(r)


def filter_by_group():
    group = input("Group name: ")
    rows = fetch("""
        SELECT c.name, c.email, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))
    print(rows)


def search_by_email():
    email = input("Email part: ")
    rows = fetch("""
        SELECT name, email FROM contacts
        WHERE email ILIKE %s
    """, (f"%{email}%",))
    print(rows)


# ---------------- SORT + PAGINATION ----------------

def paginated_view():
    limit = 3
    offset = 0

    while True:
        rows = fetch("""
            SELECT name, email, birthday
            FROM contacts
            ORDER BY name
            LIMIT %s OFFSET %s
        """, (limit, offset))

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev" and offset > 0:
            offset -= limit
        else:
            break


# ---------------- EXPORT JSON ----------------

def export_json():
    data = fetch("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
    """)

    result = []
    for d in data:
        result.append({
            "name": d[0],
            "email": d[1],
            "birthday": str(d[2]),
            "group": d[3]
        })

    with open("contacts.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Exported")


# ---------------- IMPORT JSON ----------------

def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:
        name = c["name"]

        exists = fetch("SELECT id FROM contacts WHERE name=%s", (name,))
        if exists:
            choice = input(f"{name} exists. overwrite? (y/n): ")
            if choice == "y":
                execute("DELETE FROM contacts WHERE name=%s", (name,))
            else:
                continue

        execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
        """, (name, c["email"], c["birthday"]))

    print("Imported")


# ---------------- CSV IMPORT (EXTENDED) ----------------

def import_csv():
    with open("contacts.csv", newline='') as f:
        reader = csv.DictReader(f)

        for row in reader:
            execute("""
                INSERT INTO contacts(name, email, birthday)
                VALUES (%s, %s, %s)
            """, (row["name"], row["email"], row["birthday"]))

            print("Inserted:", row["name"])


# ---------------- MAIN MENU ----------------

def menu():
    while True:
        print("""
        1 Search contacts
        2 Filter by group
        3 Search by email
        4 Pagination view
        5 Export JSON
        6 Import JSON
        7 Import CSV
        0 Exit
        """)

        choice = input("> ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            filter_by_group()
        elif choice == "3":
            search_by_email()
        elif choice == "4":
            paginated_view()
        elif choice == "5":
            export_json()
        elif choice == "6":
            import_json()
        elif choice == "7":
            import_csv()
        else:
            break


if __name__ == "__main__":
    menu()