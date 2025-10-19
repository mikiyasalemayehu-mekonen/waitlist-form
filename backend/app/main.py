from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import waitlist, admin
from .database import Base, engine
from dotenv import load_dotenv

load_dotenv()  # 👈 loads variables from .env

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(waitlist.router)
app.include_router(admin.router)
