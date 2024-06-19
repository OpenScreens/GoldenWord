import requests
from requests_oauthlib import OAuth1Session
import time

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAI2GuQEAAAAAGcnuDllrnF6ZNMp%2BMvy0pFWam9o%3DjSr1Jt307Oh6WLYiCZDWy4qf2PuHfCMlnbq9Ki0IF2U4HDAOrw'
consumer_key = 'NveXKkFiKcB11mlbaufjhnVBJ'
consumer_secret = 'KPNCv4GczrufNF652fG6FvTKEhRDss3rlV6CttSsHgFIIgqK8U'
user_id = '1803163556797460480'
access_token = '1803163556797460480-lmBsYn66xawNF4UYOdFIV1nfhnA2RN'
access_token_secret = 'FssB6hXCSwuSI9q1akoqmBpeSYv7rmIJwT9tJZwycRari'

oauth = OAuth1Session(consumer_key,consumer_secret,access_token,access_token_secret)

def check_mentions_and_reply(oauth, user_id):
    try:
        url = f"https://api.twitter.com/2/users/{user_id}/mentions"
        response = oauth.get(url)
        if response.status_code != 200:
            raise Exception(f"Request returned an error: {response.status_code} {response.text}")

        json_response = response.json()
        if 'data' in json_response:
            for mention in json_response['data']:
                tweet_id = mention['id']
                tweet_text = mention.get('text', 'No text available')
                print(f"Mention tweet ({tweet_id}) from : {tweet_text}")
                #server_response(tweet_text)
                reply_to_mention(oauth, tweet_id)
            print("Processed all mentions.")
        else:
            print("No new mentions found.")
    except Exception as e:
        print(f"Exception occurred during mention check: {str(e)}")


def reply_to_mention(oauth, tweet_id):
    try:
        url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        data = {
            "text": 'ok',
            "reply": {
                "in_reply_to_tweet_id": tweet_id
            }
        }
        response = oauth.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise Exception(f"Error replying to tweet {tweet_id}: {response.status_code} {response.text}")
        print(f"Replied to mention with tweet ID {tweet_id}.")
    except Exception as e:
        print(f"Exception occurred during reply: {str(e)}")

def server_response(tweet):
    try:
        url = "http://pingpong.test.goldenwordai.com:4998"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "message": tweet,
            "frontend": "twitter"
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise Exception(f"Error response server: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Exception occurred during response: {str(e)}")

if __name__ == "__main__":
    user_id = '1803163556797460480'

    while True:
        try:
            check_mentions_and_reply(oauth, user_id)
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
        time.sleep(60)

'''
import tweepy

# Replace with your keys and tokens
consumer_key = 'NveXKkFiKcB11mlbaufjhnVBJ'
consumer_secret = 'KPNCv4GczrufNF652fG6FvTKEhRDss3rlV6CttSsHgFIIgqK8U'
access_token = '1803163556797460480-lmBsYn66xawNF4UYOdFIV1nfhnA2RN'
access_token_secret = 'FssB6hXCSwuSI9q1akoqmBpeSYv7rmIJwT9tJZwycRari'

# Authentication with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Listener to handle mentions
class tweepy.Stream(tweepy.StreamingClient):
    def on_status(self, status):
        print(f"Nueva mención: {status.user.screen_name}: {status.text}")

    def on_error(self, status_code):
        print(f"Error en el stream: {status_code}")

# Initialize Tweepy API
api = tweepy.API(auth)

# Define a function to start streaming
def start_streaming(listener, track):
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(track=track)

# Define the track keyword or mention
track = ['@PingPongLLM']  # Replace with your Twitter handle or keyword

# Keep the program running (optional, depending on your environment)
while True:
    try:
        start_streaming(MentionListener(), track)
    except Exception as e:
        print(f"Error: {e}")
'''

