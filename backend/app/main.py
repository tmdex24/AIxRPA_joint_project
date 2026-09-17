from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def home():
    return {"AIxRPA API radi! :)"}