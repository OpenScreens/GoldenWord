You should get an app access token, if your app only calls APIs that don’t require the user’s permission to access the resource. But if your app also calls APIs that require a user access token, you should just get a user access token because in most cases you can use the user access token to call APIs that accept app access tokens. The exception is if you call the EventSub APIs (for example, Create EventSub Subscription). If you call the EventSub APIs and use webhooks, you must also get an app access token because the calls fail if you try to use a user access token.

https://dev.twitch.tv/docs/api/reference/#create-eventsub-subscription
eee

{
    "data": [
        {
            "id": "1063475030",
            "login": "pingpongtb",
            "display_name": "pingpongtb",
            "type": "",
            "broadcaster_type": "",
            "description": "",
            "profile_image_url": "https://static-cdn.jtvnw.net/user-default-pictures-uv/ce57700a-def9-11e9-842d-784f43822e80-profile_image-300x300.png",
            "offline_image_url": "",
            "view_count": 0,
            "created_at": "2024-04-08T13:21:58Z"
        }
    ]
}

client id:        pfmyo3749gxj2yyatlsjwazrr5zhzn
secret:           hco9h9q5sudkadqgp2t53hps1oqrxl
App Access Token: 

{
    "access_token": "x9toyqcnjp7efn3abm2ugjaqbhd8x7",
    "expires_in": 5556888,
    "token_type": "bearer"
}


https://id.twitch.tv/oauth2/authorize?client_id=pfmyo3749gxj2yyatlsjwazrr5zhzn&redirect_uri=http%3A%2F%2Flocalhost%3A3000&response_type=code&scope=user%3Aread%3Achat+user%3Abot+channel%3Abot&state=1kgA9xe7LidiRV71TmgSOQ%3D%3D

http://localhost:3000/?code=im5qxdaw5v9kjbeuyr7ygdo0118orp&scope=user%3Aread%3Achat+user%3Abot+channel%3Abot&state=1kgA9xe7LidiRV71TmgSOQ%3D%3D
