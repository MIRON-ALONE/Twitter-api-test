import tweepy
import os


api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
accses_token = os.getenv('ACCESS_TOKEN')
accses_secret = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(accses_token, accses_secret)

api = tweepy.API(auth)


def like_tweet(status_id):
    try:
        api.create_favorite(status_id)
        print(f"Complete: {status_id} ")
    except tweepy.TweepyException as e:
        print(f"Error: {e.response.status_code} - {e.response.text}")

status_id = "1878132133144715658"  
api.create_favorite(status_id)

print("Complete")
   
