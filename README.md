Pyong

Ping pong has a huge role in the company I work in, so I decided that I was going to create a service where we could keep scores of all matches done throughout all offices.

In the future, based on the information collected I would then generate statistics per player and per office that could be consumed to keep scores for different tournaments or local competitions.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Gunicorn](https://gunicorn.org/) is a Python WSGI HTTP Server for UNIX. We will use it to provide a nice setup for online platforms such as AWS or Heroku.

## Database Setup
With Postgres running, create a new database and add the name in the setup.sh that is used as environment variables for the app:
```bash
createdb pyong-dev
```
**Note:** Make sure that you are using the correct owner for the database, else add `-U <username>`.

## Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
or a production environment:
```bash
gunicorn app:app
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use that file to find and start the application. 

## Authorization
**Important:** 
> `GET` and `POST` endpoints for players and matches require authorization role **Player**

> For `PATCH` and `DELETE` endpoints you require authorization role **Admin**

All authorization roles can *only* be given through Auth0 roles  
## API Endpoints
 
### GET `/`
- This is the initial endpoint initial request page, this is only to ensure the endpoint works properly.
- Request Arguments: None
- Returns: message with "Hello!!!!!". 

### GET `/login`
- redirect link to Auth0 login process.
- Request Arguments: None

### GET `/callback`
- After a successful login using Auth0 process, it will redirect you back to this site with a new authentication token.
- Request Arguments: None
- Returns: None

### GET `/players`
- Endpoint to receive list of players.
- Request Arguments: None.
- Returns: returns a success parameter along with an array of players.
```
{
    "players": [
        {
            "email": "player@mail.com",
            "id": 1,
            "match_a": [...],
            "match_b": [...],
            "name": "Player Name"
        },
       	...
    ],
    "success": true
}
```
### POST `/players`
- Endpoint to create a new player.
- Request Arguments: `{ name:"", email:"" }`.
- Returns: returns a success parameter along with player id.
```
{
  'success': true,
  'created': id,
}
```
### GET `/matches`
- Endpoint to get matches between two players.
- Request Arguments: **optional**: page=int, used for pagination shows 10 at a time.
- Returns: returns an array of matches.
```
{
    "matches": [
        {
            "date": "Sat, 18 Jan 2020 21:54:26 GMT",
            "id": 2,
            "playerA": "player1",
            "playerB": "player2",
            "scoreA": 5,
            "scoreB": 4
        },
        ...
    ],
    "success": true
}
```
### POST `/matches`
- Endpoint to create a new match between to players.
- Request Arguments: `{ "scoreA": number, "scoreB": number, "playerA": player.id, "playerB": player2.id }`.
- Returns: returns a success parameter along with the created match id and date.
```
{
    "created": 10,
    "date": "Mon, 20 Jan 2020 23:07:56 GMT",
    "success": true
}
```
### PATCH `/matches/<int:match_id>`
- Endpoint to edit the score of an existing match.
- Request Arguments: `{ "scoreA": number, "scoreB": number }`.
- Returns: returns a success parameter along with complete information of the match updated.
```
{
    "match": {
        "date": "Sat, 18 Jan 2020 21:54:26 GMT",
        "id": match.id,
        "playerA": "player1",
        "playerB": "player2",
        "scoreA": 5,
        "scoreB": 4
    },
    "success": true
}
```
### DELETE `/matches/<int:match_id>`
- Endpoint to delete a match with given question id.
- Request Arguments: None.
- Returns: returns a success parameter along with the delete id as confirmation.
```
{
  'success': true,
  'deleted': match_id,
}
```
## Failed attempts
All failed attempts to the api will include a message with a brief description of the problem.

Example:
```
{
  'success': false,
  'error': 404,
  'message": "resource not found"
}
```

## Testing
To run the tests, use the provided `postman_collection.json` file running on [Postman](https://www.getpostman.com/)