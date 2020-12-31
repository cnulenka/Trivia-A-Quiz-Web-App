# Trivia-A-Quiz-Web-App

This is a fun quiz game where people can test their knowledge on fields of Science, Art, Geography, History, Entertainment, Sports.

1) First page displays all questions(10 per page), has filter to display questions by each category.
2) Each Question frame has a question, category and difficulty rating and a toggle to show/hide the answer. 
3) Ability to delete questions.
4) Form to add new questions.
5) Search Bar to search for questions based on a text query string.
6) Functionality to play the quiz game, randomizing questions either across all categories or a specific one. 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3.7, pip and node installed on their local machines.

### Frontend Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Running Your Frontend in Dev Mode

The frontend app is built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 
The application runs on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable
* 500 - server error

### Endpoints

#### GET /categories
* General
	* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
	* Request Arguments: None
	* Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
* Sample: `curl http://127.0.0.1:5000/categories`<br>

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "success": true
        }

#### GET /questions

* General:
  * Returns a list questions.
  * Results are paginated in groups of 10. Default page is 1.
  * Also returns list of categories and total number of questions.
* Sample: `curl http://127.0.0.1:5000/questions`<br>

        {
            "categories": {
                            "1": "Science",
                            "2": "Art",
                            "3": "Geography",
                            "4": "History",
                            "5": "Entertainment",
                            "6": "Sports"
                        },
            "current_category": null,
            "questions": [
                            {
                                "answer": "Apollo 13",
                                "category": 5,
                                "difficulty": 4,
                                "id": 2,
                                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                            },
                            {
                                "answer": "Tom Cruise",
                                "category": 5,
                                "difficulty": 4,
                                "id": 4,
                                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                            },
                            {
                                "answer": "Maya Angelou",
                                "category": 4,
                                "difficulty": 2,
                                "id": 5,
                                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                            },
                            {
                                "answer": "Edward Scissorhands",
                                "category": 5,
                                "difficulty": 3,
                                "id": 6,
                                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                            },
                            {
                                "answer": "Muhammad Ali",
                                "category": 4,
                                "difficulty": 1,
                                "id": 9,
                                "question": "What boxer's original name is Cassius Clay?"
                            },
                            {
                                "answer": "Brazil",
                                "category": 6,
                                "difficulty": 3,
                                "id": 10,
                                "question": "Which is the only team to play in every soccer World Cup tournament?"
                            },
                            {
                                "answer": "Uruguay",
                                "category": 6,
                                "difficulty": 4,
                                "id": 11,
                                "question": "Which country won the first ever soccer World Cup in 1930?"
                            },
                            {
                                "answer": "George Washington Carver",
                                "category": 4,
                                "difficulty": 2,
                                "id": 12,
                                "question": "Who invented Peanut Butter?"
                            },
                            {
                                "answer": "Lake Victoria",
                                "category": 3,
                                "difficulty": 2,
                                "id": 13,
                                "question": "What is the largest lake in Africa?"
                            },
                            {
                                "answer": "The Palace of Versailles",
                                "category": 3,
                                "difficulty": 3,
                                "id": 14,
                                "question": "In which royal palace would you find the Hall of Mirrors?"
                            }
                        ],
            "success": true,
            "total_questions": 19
        }

#### DELETE /questions/\<int:id\>

* General:
  * Deletes a question by id, using url parameters.
  * Returns JSON with success upon successful deletion.
* Sample: `curl http://127.0.0.1:5000/questions/5 -X DELETE`<br>

        {
            "success": True
        }

#### POST /questions

This endpoint serves two purposes, it either creates a new question or returns search results.

1. If <strong>no</strong> search term is included in request:

* General:
  * Creates a new question using the submitted question, answer, difficulty and category.
  * Returns JSON object with newly created question id upon success.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "In which Indian state is Shree Jagannath Temple located?",
            "answer": "Odisha",
            "difficulty": 3,
            "category": "3"
        }'`<br>

        {
            "newQuestionId": 24,
            "success": true
        }


2. If search term <strong>is</strong> included in request:

* General:
  * Searches for questions using search term in JSON request parameters.
  * Returns JSON object with paginated questions, returns any questions for whom the search term is a
    substring.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "tom"}'`<br>

        {
            "currentCategory": null,
            "questions": [
                            {
                                "answer": "Apollo 13",
                                "category": 5,
                                "difficulty": 4,
                                "id": 2,
                                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                            }
                        ],
            "success": true,
            "totalQuestions": 1
        }

#### GET /categories/\<int:id\>/questions

* General:
  * Gets questions by category id using url parameters.
  * Returns JSON object with paginated matching questions in groups of 10.
* Sample: `curl http://127.0.0.1:5000/categories/1/questions`<br>

        {
            "currentCategory": 3,
            "questions": [
                            {
                                "answer": "Lake Victoria",
                                "category": 3,
                                "difficulty": 2,
                                "id": 13,
                                "question": "What is the largest lake in Africa?"
                            },
                            {
                                "answer": "The Palace of Versailles",
                                "category": 3,
                                "difficulty": 3,
                                "id": 14,
                                "question": "In which royal palace would you find the Hall of Mirrors?"
                            },
                            {
                                "answer": "Agra",
                                "category": 3,
                                "difficulty": 2,
                                "id": 15,
                                "question": "The Taj Mahal is located in which Indian city?"
                            }
                        ],
            "success": true,
            "totalQuestions": 3
        }

#### POST /quizzes

* General:
  * Serves the quiz game to the users.
  * Uses JSON request parameters of category and previous questions.
  * Returns JSON object with a random question not included in previous questions.
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [13],
                                            "quiz_category" : {"type": "Geography", "id": "3"}}'`

```json
{
    "question": {
                    "answer": "Agra",
                    "category": 3,
                    "difficulty": 2,
                    "id": 15,
                    "question": "The Taj Mahal is located in which Indian city?"
                },
    "success": true
}

```

## Authors

Shakti Prasad Lenka worked on the Backend APIs (`__init__.py`), test suite (`test_flaskr.py`), and this README.<br>
Frontend and other started code, were created by [Udacity](https://www.udacity.com/) as a project template for the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).
