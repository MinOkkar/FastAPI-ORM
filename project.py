from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATABASE_URL = "mysql+pymysql://root@localhost:3306/animelist"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    animes = relationship("Anime", secondary="anime_genres", back_populates="genres")

class Anime(Base):
    __tablename__ = "animes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


    genres = relationship("Genre", secondary="anime_genres", back_populates="animes")

anime_genre = Table(
    "anime_genres",
    Base.metadata,
    Column("anime_id", Integer, ForeignKey("animes.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True)
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#routes

@app.get("/animes/")
def get_animes(db: Session = Depends(get_db)):
    animes = db.query(Anime).all()
    return [{"id": anime.id, "name": anime.name} for anime in animes]


@app.post("/animes/")
def create_anime(anime: dict = Body(...), db: Session = Depends(get_db)):
    name = anime.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Please Enter anime name")
    new_anime = Anime(name=name)
    db.add(new_anime)
    db.commit()
    db.refresh(new_anime)
    return {"id": new_anime.id, "name": new_anime.name}

@app.post("/genres/")
def create_genre(genre: dict = Body(...), db: Session = Depends(get_db)):
    name = genre.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Please Enter genre name")
    new_genre = Genre(name=name)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return{"id": new_genre.id, "name": new_genre.name}


@app.post("/add_genres/")
def add_genres(genreadd: dict = Body(...), db: Session = Depends(get_db)):
    anime_id = genreadd.get("anime_id")
    genre_id = genreadd.get("genre_id")


    if not anime_id or not genre_id:
        raise HTTPException(status_code=400, detail="anime/genre id are required")


    anime = db.query(Anime).filter(Anime.id == anime_id).first()
    genre = db.query(Genre).filter(Genre.id == genre_id).first()


    if not anime:
        raise HTTPException(status_code=404, detail="anime not found")
    if not genre:
        raise HTTPException(status_code=404, detail="genre not found")


    anime.genres.append(genre)
    db.commit()


    return {"message": f"{anime.name} is now in {genre.name} genre"}


@app.get("/animes/{anime_id}")
def get_anime_genres(anime_id: int, db: Session = Depends(get_db)):
    anime = db.query(Anime).filter(Anime.id == anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")

    return [{"id": genre.id, "name": genre.name} for genre in anime.genres]

@app.get("/genres/{genre_id}")
def get_genre_animes(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")


    return [{"id": anime.id, "name": anime.name} for anime in genre.animes]