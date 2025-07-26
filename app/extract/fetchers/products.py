import requests 
import psycopg2

# Configuration
API_URL = "https://fakestoreapi.com/products"
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "fakestore",
    "user": "sunnakh",
    "password": "passwordpwrd",
}


def fetch_products():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching products from API:", e)
        return []


def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return None


def create_table(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY,
            title TEXT,
            price NUMERIC,
            description TEXT,
            category TEXT,
            image TEXT
        );
    """
    )


def insert_products(cursor, products):
    for product in products:
        cursor.execute(
            """
            INSERT INTO product (
                id, title, price, description, category, image
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                product["id"],
                product["title"],
                product["price"],
                product["description"],
                product["category"],
                product["image"],
            ),
        )


def main():
    # Fetch data from API
    products = fetch_products()
    if not products:
        print("No products to insert. Exiting.")
        return

    # Connect to database
    conn = connect_to_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        create_table(cursor)
        insert_products(cursor, products)
        conn.commit()
        print(f"Inserted {len(products)} products into PostgreSQL successfully.")
    except psycopg2.Error as e:
        print("Database error:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection closed.")


if __name__ == "__main__":
    main()
