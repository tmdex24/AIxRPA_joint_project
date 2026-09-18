import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=int(DB_PORT)
        )

    except Exception as e:
        raise Exception(f"Neuspelo povezivanje na bazu: {e}")

    return conn

def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute ("""CREATE TABLE IF NOT EXISTS invoices(
                            ID VARCHAR(36) PRIMARY KEY,
                            file_name VARCHAR(255),
                            created_at TIMESTAMP,
                            status_obrade VARCHAR(20),
                            document_text TEXT,
                            invoice_number VARCHAR(50),
                            date_of_issue DATE,
                            client_name VARCHAR(100),
                            PIB VARCHAR(20),
                            amount DECIMAL(10,2),
                            currency VARCHAR(4))""")
    connection.commit()
    cursor.close()
    connection.close()

