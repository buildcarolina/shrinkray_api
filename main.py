import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import Session, select
from db import get_session

from models.urls import Urls

app = FastAPI()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost:5173"
]

# Add the CORS middleware...
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/urls")
async def get_all_urls(session: Session = Depends(get_session)):
    statement = select(Urls)
    print(f"SQL Statement is: {statement}")
    results = session.exec(statement).all()
    return results


@app.get("/urls/{id}")
async def get_single_url(id: str, session: Session = Depends(get_session)):
    statement = select(Urls).where(Urls.id == id)
    result = session.exec(statement).one()

    return result


@app.post("/urls/add")
async def add_url(title: str, url: str):
    return {title: url}

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
