import psycopg2
from ..config import raw_postgresql_connection_string


def get_conn():

    # Connect to the PostgreSQL database using the connection string
    conn = psycopg2.connect(raw_postgresql_connection_string)

    return conn


def clear_table(collection_name: str) -> bool:
    try:
        conn = get_conn()

        cur = conn.cursor()

        # Execute the DELETE statement to remove all rows from the collection
        cur.execute(f"DELETE FROM {collection_name}")

        # Commit the transaction
        conn.commit()

        cur.close()
        conn.close()

        print(f"Cleared table {collection_name}")
        return True
    except Exception as e:
        print(f"Unable to clear {collection_name}: {e}")
        return False
