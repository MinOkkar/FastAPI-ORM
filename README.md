## Dependicies

-FastAPI – The web framework to build the API.

-SQLAlchemy – For database ORM functionality.

-pymysql – For MySQL database connection (used by SQLAlchemy).

-Uvicorn – The ASGI server to run the FastAPI application.


```bash
pip install -r requirements.txt
```

## API Endpoints

### 1. Get a list of all animes:
- **Endpoint**: `GET /animes/`
- **Response**: List of all anime names and IDs.

### 2. Create a new anime:
- **Endpoint**: `POST /animes/`
- **Body**: `{"name": "Naruto"}`
- **Response**: The created anime's ID and name.

### 3. Create a new genre:
- **Endpoint**: `POST /genres/`
- **Body**: `{"name": "Action"}`
- **Response**: The created genre's ID and name.

### 4. Add a genre to an anime:
- **Endpoint**: `POST /add_genres/`
- **Body**: `{"anime_id": 1, "genre_id": 1}`
- **Response**: Confirmation message.

### 5. Get genres of a specific anime:
- **Endpoint**: `GET /animes/{anime_id}`
- **Response**: List of genres for the anime.

### 6. Get animes of a specific genre:
- **Endpoint**: `GET /genres/{genre_id}`
- **Response**: List of animes for the genre.
