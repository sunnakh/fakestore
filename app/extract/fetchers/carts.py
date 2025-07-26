# carts.py
import requests
import psycopg2

# Configuration
API_URL = "https://fakestoreapi.com/carts"
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "fakestore",
    "user": "sunnakh",
    "password": "passwordpwrd",
}


def fetch_carts():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching carts from API:", e)
        return []


def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return None


def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY,
            userId INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart_product (
            cart_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            PRIMARY KEY (cart_id, product_id),
            FOREIGN KEY (cart_id) REFERENCES cart(id)
        );
    """)


def insert_carts(cursor, carts):
    for cart in carts:
        cursor.execute(
            """
            INSERT INTO cart (id, userId)
            VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (cart["id"], cart["userId"])
        )

        for product in cart["products"]:
            cursor.execute(
                """
                INSERT INTO cart_product (cart_id, product_id, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT (cart_id, product_id) DO NOTHING;
            """,
                (cart["id"], product["productId"], product["quantity"])
            )


def main():
    carts = fetch_carts()
    if not carts:
        print("No carts to insert. Exiting.")
        return

    conn = connect_to_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        create_tables(cursor)
        insert_carts(cursor, carts)
        conn.commit()
        print(f"Inserted {len(carts)} carts into PostgreSQL successfully.")
    except psycopg2.Error as e:
        print("Database error:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection closed.")


if __name__ == "__main__":
    main()
