from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes.pdf_routes import router as pdf_router
from database.db_connection import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # ovde ide cleanup kod, ako ti treba (npr. zatvaranje konekcija)

app = FastAPI(lifespan=lifespan)
app.include_router(pdf_router)

@app.get("/")
def home():
    return {"AIxRPA API radi! :)"}
