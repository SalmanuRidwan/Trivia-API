# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Trivia API Documentation

- `GET /categories`

  - Returns an object with a single key **categories**, that contains an object of `id: category_string` key: value pairs.
  - URI: `http://localhost:5000/categories`
  - Response :
 
    ```json
   "categories":   {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
      }
    ```

- `GET /questions`

  - Returns all the questions with their respective answers, and total number of questions
  - Questions are paginated by 10
  - URI: `http://localhost:5000/questions?page=$(id)`
  - Response:

    ```
    
    {
        "categories":{
            "1":"Science",
            "2":"Art",
            "3":"Geography",
            "4":"History",
            "5":"Entertainment",
            "6":"Sports"
            },
        "questions":[
            {
            "answer":"Muhammad Ali",
            "category":4,
            "difficulty":1,
            "id":9,
            "question":"What boxer's original name is Cassius Clay?"
            },
            {
            "answer":"Brazil",
            "category":6,
            "difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
            },
            {
            "answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
            }],
        "success":true,
        "total_questions":3}
    ```

- POST `/questions`
  
    - Adds a new value to the object *question*
    - Returns a success value on successful request
    - URI: `curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"answer": 2, "category": 2, "diffuculty": 1, "question": "A car has how many side mirrors?"}'`
    - Response:
    - 
        ```
            "success": True,
        ```

- POST `/search`
    - Searches for question(s) using partial string matching
    - Search is Case in-sensitive
    - URI: `curl http://localhost:5000/questions?search="world"`
    - Response:
  
    ```
    {
        "answer":"Brazil",
        "category":6,
        "difficulty":3,
        "id":10,
        "question":"Which is the only team to play in every soccer World Cup tournament?"
    },
    {
        "answer":"Uruguay",
        "category":6,
        "difficulty":4,
        "id":11,
        "question":"Which country won the first ever soccer World Cup in 1930?"
    }
    ```

- DELETE `/questions/<int:question_id>`
  - Deletes a specific question based on the id provided
  - Returns success value *i.e* True, total questions count and the remaining questions available
  - URI: `curl http://localhost:5000/question/9 -X DELETE -H "Content-Type: application/json"`

> In reference to GET `/questions` above

  - Response:

```
    
    {
        "categories":{
            "1":"Science",
            "2":"Art",
            "3":"Geography",
            "4":"History",
            "5":"Entertainment",
            "6":"Sports"
            },
        "questions":[
            {
            "answer":"Brazil",
            "category":6,
            "difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
            },
            {
            "answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
            }],
        "success":true,
        "total_questions":2}
```


- POST `/quizzes`
  - For submitting answers to the questions in the game
  - On successful request, it returns the question_id, question and answer of a specific question
  - URI: `curl http://localhost:5000/categories/9/questions -X POST`
  - Response:

````
    "answer":"Muhammad Ali",
    "id":9,
    "question":"What boxer's original name is Cassius Clay?"
````

  
## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
