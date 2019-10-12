
# socnet-rest

Django rest application with postgresql Docker container



## Dependencies
You will need [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/), Python and [invoke module](http://www.pyinvoke.org/) to use this application

## How to use the module
run docker container to create postgresql-database:
`
inv start-docker
`
if you want to see the running containers:
```
docker ps
```

next, to create virtual environment and migrate tables,  run the following command :
`
inv migrate
`

after this, you will be able to see empty tables into db **(127.0.0.1:542, user='postgres',psw='', db='postgres')**



 ## application endpoints
|`id`|`http method`|url| parameters example|
|--|------------------|-----------|--------------|
|`1`|`POST`|http://127.0.0.1:8000/api/users|  {    "username": "test",   "password":"test" "email": "adnn@yahoo.com",    "first_name": "",    "last_name": ""}
|`2`|`POST`|http://127.0.0.1:8000/api/auth|{    "username": "test",    "password": "test",   }
|`3`|`GET`|http://127.0.0.1:8000/api/posts/| `token` 
|`4`|`POST`|http://127.0.0.1:8000/api/posts/2/| `token` , {"text":"example"}
|`5`|`GET`|http://127.0.0.1:8000/api/posts/| `token` 
|`5`|`GET`|http://127.0.0.1:8000/api/posts/2/likes/| `token` 
|`4`|`POST`|http://127.0.0.1:8000/api/posts/2/likes/| `token` 

I am also attaching postman file `socnet.postman_collection.json` to make easy testing process.


## Run Bot

to run the bot, you need the following command:
```bash
$ inv execute-bot
```


application also includes api keys of `clearbit` and `emailhunder` in order to make easy their usage (just update social_net/settings.py `USE_EMAILHUNTER` and `USE_CLEARBIT` values.)


