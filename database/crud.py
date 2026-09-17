from database.db_connection import get_connection

def insert_invoice(id, file_name, status):
    '''
    GUID praviti u trenutku primanja fajla preko fast apija, 
    renemovati fajl po potrebi kao GUID_nesto.pdf
    '''
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO invoices (ID, file_name, created_at, status_obrade) VALUES (%s, %s, NOW(), %s)", (id, file_name, status))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def insert_invoice(id, file_name, status):
    '''
    GUID praviti u trenutku primanja fajla preko fast apija, 
    renemovati fajl po potrebi kao GUID_nesto.pdf
    '''
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO invoices (ID, file_name, created_at, status_obrade) VALUES (%s, %s, NOW(), %s)", (id, file_name, status))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def update_invoice_data(id, document_text, date_of_issue, client_name, pib, amount, status):
    '''
    date_of_issue mora biti u formatu "2026-01-15"
    '''
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE invoices 
                        SET document_text=%s, date_of_issue = %s, client_name = %s, PIB = %s, amount = %s, status_obrade = %s  
                        WHERE ID = %s""", (document_text, date_of_issue, client_name, pib, amount, status, id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_invoice_text(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT document_text FROM invoices WHERE ID= %s""", (id,))

        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"Faktura sa ID {id} ne postoji")

        return row[0]
    finally:
        cursor.close()
        conn.close()


