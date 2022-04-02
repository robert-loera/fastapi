from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# this is for the sql alchemy to create the tables in postgres
# dont need when we use alembic
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# domains that we can set to access our api
origins = ['https://www.google.com']

# basically a function that is run before every request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# this was used when we were using sql
# # connecting to postgres database
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='fastapi', user='postgres', password='loera007', cursor_factory=RealDictCursor)
#         curr = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print(error)
#         time.sleep(5)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World!!!"}
