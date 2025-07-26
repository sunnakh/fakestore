import requests 
import psycopg2

# Configuration
API_URL = "https://fakestoreapi.com/users"
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "fakestore",
    "user": "sunnakh",
    "password": "passwordpwrd",
}


def fetch_users():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching users from API:", e)
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
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT,
            password TEXT
        );
    """
    )


def insert_users(cursor, users):
    for user in users:
        cursor.execute(
            """
            INSERT INTO users (
                id, username, email, password
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                user["id"],
                user["username"],
                user["email"],
                user["password"],
            ),
        )


def main():
    # Fetch data from API
    users = fetch_users()
    if not users:
        print("No users to insert. Exiting.")
        return

    # Connect to database
    conn = connect_to_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        create_table(cursor)
        insert_users(cursor, users)
        conn.commit()
        print(f"Inserted {len(users)} users into PostgreSQL successfully.")
    except psycopg2.Error as e:
        print("Database error:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection closed.")


if __name__ == "__main__":
    main()
