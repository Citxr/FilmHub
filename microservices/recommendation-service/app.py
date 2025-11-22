from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random

app = FastAPI(title="Сервис рекомендаций", version="1.0.0")


class GenreRequest(BaseModel):
    genres: List[str]


class MovieRecommendation(BaseModel):
    id: int
    title: str
    genre: str


movies_db = [
    {"id": 1, "title": "Начало", "жанр": "фантастика"},
    {"id": 2, "title": "Побег из шоушенка", "жанр": "драма"},
    {"id": 3, "title": "Темный рыцарь", "жанр": "боевик"},
    {"id": 4, "title": "Криминальное чтиво", "жанр": "криминал"},
    {"id": 5, "title": "Форест гамп", "жанр": "драма"},
    {"id": 6, "title": "Матрица", "жанр": "фантастика"},
    {"id": 7, "title": "Крёстный отец", "жанр": "криминал"},
    {"id": 8, "title": "Интерстеллар", "жанр": "фантастика"},
    {"id": 9, "title": "Бойцовский клуб", "жанр": "драма"},
    {"id": 10, "title": "Славные парни", "жанр": "криминал"},
]


@app.get("/")
def read_root():
    return {"message": "Сервис рекомендаций запущен!"}


@app.post("/recommend/", response_model=List[MovieRecommendation])
def get_recommendations(genre_request: GenreRequest):
    if not genre_request.genres:
        raise HTTPException(status_code=400, detail="Не найдено фильмов по жанру")

    filtered_movies = [movie for movie in movies_db if movie["жанр"] in genre_request.genres]

    if not filtered_movies:
        filtered_movies = movies_db

    recommendations = random.sample(filtered_movies, min(3, len(filtered_movies)))

    return recommendations


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)