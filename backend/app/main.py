from fastapi import FastAPI
from .routes.pdf_routes import router as pdf_router




app = FastAPI()
app.include_router(pdf_router) # ovim smo povezali app i router i samim tim app moze da koristi rutu /upload

@app.get("/")
def home():
    return {"AIxRPA API radi! :)"}
