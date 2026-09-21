@app.get("/test-db")
def test_db():

    insert_invoice(
        "test-id",
        "test.pdf",
        "PROCESSING"
    )

    return {"status": "ok"}
