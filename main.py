# Github: https://github.com/Priyanshu-Gupta2101/Url_shortener
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, HttpUrl
import random, os, string
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_code = Column(String(6), unique=True, index=True)


Base.metadata.create_all(bind=engine)
app = FastAPI()


class URLInput(BaseModel):
    url: HttpUrl


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.post("/shorten")
def shorten_url(url_input: URLInput, db: Session = Depends(get_db)):

    parsed_url = urlparse(str(url_input.url))
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    if parsed_url.query:
        normalized_url += f"?{parsed_url.query}"

    existing_url = db.query(URL).filter(URL.original_url == normalized_url).first()
    if existing_url:
        return {"short_url": f"{app.url_path_for('redirect_to_original', short_code=existing_url.short_code)}"}

    for _ in range(5):
        short_code = create_short_code()
        db_url = URL(original_url=normalized_url, short_code=short_code)
        try:
            db.add(db_url)
            db.commit()
            return {"short_url": f"{app.url_path_for('redirect_to_original', short_code=short_code)}"}
        except IntegrityError:
            db.rollback()

    raise HTTPException(status_code=500, detail="Failed to generate a unique short code")


@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    original_url = db_url.original_url
    return RedirectResponse(original_url)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)

