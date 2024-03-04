from typing import Optional, List
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# from . import models
from database import engine , get_db
from sqlalchemy.orm import Session
import models, schemas, utils
from routers import user, post, auth,vote
from config import Settings
#Create tables to database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origin=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials= True,
    allow_headers=["*"],
    allow_methods=["*"]
)


while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi', user='postgres',
                                password='root', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database conectionn successful")
        break
    except Exception as error:
        print("Database conectionn FAILED")
        print("Error :", error)
        time.sleep(2)
    
@app.get("/")
async def root():
    return {"message":"Joe nalz"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




