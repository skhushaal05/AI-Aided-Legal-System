from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Running for legal app 2"}