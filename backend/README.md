# Full Stack Trivia API Backend

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

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
#psql trivia < trivia.psql
psql test2 < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 



## Testing
To run the tests, run
```
dropdb test1_test
createdb test1_test
psql test1_test < test1.psql
python test_flaskr.py
```


API Reference
Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.
Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return two error types when requests fail:

404: Resource Not Found
422: Not Processable


Endpoints
GET /getquestions
General:
Returns a list of questions objects, success value, and total number of questions
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/getquestions
   
  {
   "categories":
       {
           "1":"Science",
           "2":"Art",
           "3":"Geography",
           "4":"History",
           "5":"Entertainment",
           "6":"Sports"
       },
   "questions":
       [
           {"answer":"Tom Cruise","category":5,"difficulty":4,"id":4,
           "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},
           {"answer":"Maya Angelou",
           "category":4,"difficulty":2,"id":5,
           "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
           {"answer":"Muhammad Ali",
           "category":4,"difficulty":1,"id":9,
           "question":"What boxer's original name is Cassius Clay?"}
           ,{"answer":"Brazil",
           "category":6,"difficulty":3,"id":10,
           "question":"Which is the only team to play in every soccer World Cup tournament?"},
           {"answer":"Uruguay",
           "category":6,"difficulty":4,"id":11,
           "question":"Which country won the first ever soccer World Cup in 1930?"},
           {"answer":"George Washington Carver",
           "category":4,"difficulty":2,"id":12,
           "question":"Who invented Peanut Butter?"},
           {"answer":"Lake Victoria",
           "category":3,"difficulty":2,"id":13,
           "question":"What is the largest lake in Africa?"},
           {"answer":"The Palace of Versailles",
           "category":3,"difficulty":3,"id":14,
           "question":"In which royal palace would you find the Hall of Mirrors?"},
           {"answer":"Escher",
           "category":2,"difficulty":1,"id":16,
           "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"},
           {"answer":"Mona Lisa",
           "category":2,"difficulty":3,"id":17,
           "question":"La Giaconda is better known as what?"}
       ],
   "success":true,
   "total_questions":93
  }
   
   
   
   
   
POST /addquestions
General:
Creates a new qeustions using the submitted quesion, answer , category and difficulty. Returns all data of the created questions, success value.
curl -d '{"question":"Question Text" , "answer":"Answer Text" , "difficulty":"2" , "category":"2" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/addquestions

{
    "data": 
        {
        "answer":"Answer Text",
         "category":"2",
         "difficulty":"2",
         "question":"Question Text"
         },
     "success":true
}




DELETE /questionsdelete/{question_id}
General:
Deletes the question of the given ID if it exists. Returns the id of the deleted questions, success value.
curl http://127.0.0.1:5000/questionsdelete/2
{
    "success": True,
    "data": "delete",
    "deleted": question_id
}



POST / questionssearch
General:
it is used for search specif terms useing submite search term. It returns a json questions list with all questions that mucht the term and total question that found.
curl -d '{"searchTerm":"why"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/questionssearch

{
    "questions":
        [
            {
                "answer":"Maya Angelou",
                "category":4,
                "difficulty":2,
                "id":5,
                "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }
        ],
    "success":true,
    "total_questions":1
}


GET / categories
General:
It returns a json that has all categories with their IDs.
curl http://127.0.0.1:5000/categories

{
    "categories":
        {
            "1":"Science",
            "2":"Art",
            "3":"Geography",
            "4":"History",
            "5":"Entertainment",
            "6":"Sports"
        },
    "success":true
}

POST / 
General:
It returns one new question that match the request's category. It then tack the old questions and add them to old list and then generate new question that is not in the old question lis.
curl -d '{ "previous_questions":"" , "quiz_category" :"{type: "History", id: "4"}"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/quizzes

{
    "questions":
        [
            {
                "answer":"Maya Angelou",
                "category":4,
                "difficulty":2,
                "id":5,
                "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }
        ],
    "success":true,
}

