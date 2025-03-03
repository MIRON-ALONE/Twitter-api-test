import tweepy
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
accses_token = os.getenv('ACCESS_TOKEN')
accses_secret = os.getenv('ACCESS_SECRET')
domain = os.getenv('RAILWAY_PUBLIC_DOMAIN')
def get_oauth_handler():
    return tweepy.OAuth1UserHandler(consumer_key=api_key, consumer_secret=api_secret, callback="http://localhost:5501/index.html")

oauth_sessions = {}


@app.get("/auth/login")
async def login():
    auth = get_oauth_handler()
    try:
        auth_url = auth.get_authorization_url()
        oauth_sessions[auth.request_token["oauth_token"]] = auth.request_token["oauth_token_secret"]
        return {"auth_url": auth_url} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка авторизации: {str(e)}")


@app.get("/auth/callback")
async def auth_callback(oauth_token: str, oauth_verifier: str):
    auth = get_oauth_handler()
    auth.request_token = {
        "oauth_token": oauth_token,
        "oauth_token_secret": oauth_sessions.pop(oauth_token),
    }
    access_token, access_token_secret = auth.get_access_token(oauth_verifier)
 
    response = JSONResponse(status_code=200, content={"access_token": access_token})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600,
        secure=True,
        samesite="none",
        path="/"
    )
#временное решение, лучше хранить данные о access_token_secret, oauth_token_secret в базе данных
    response.set_cookie(
        key="access_token_secret",
        value=access_token_secret,
        httponly=True,
        max_age=3600,
        secure=True,
        samesite="none",
        path="/"
    )

    return response


@app.post("/tweets/{id}/like")
async def like_tweet(request: Request, id:int):
    access_token = request.cookies.get("access_token")
    access_token_secret = request.cookies.get("access_token_secret")


    client = tweepy.Client(   
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    response = client.like(
        tweet_id=id,
        user_auth=True
    )

    return response