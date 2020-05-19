# Full Stack Trivia API Backend

# 
# Introduction
# 

## Getting Started
- Base URL: The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration. The frontend is hosted at http://127.0.0.1:30000/. 
- Authentication: This version of the application does not require authentication or API keys. 

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
psql trivia < trivia.psql
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



## Error Handling

- Errors are returned as JSON objects in the following format: 
    ```
    {
        "success": False, 
        "error": 404,
        "message": "Not found"
    }
    ```
- The API will return two error types when requests fail:
    - 404: Resource Not Found
    - 422: Not processable

## Resource Endpoint Library

- GET /categories
    - General: 
        - Returns a list of categories, success value, and total number of categories
    - Sample:
        - curl http://127.0.0.1:5000/categories
        ```
        {
            "categories": [
                "Science",
                "Art",
                "Geography",
                "History",
                "Entertainment",
                "Sports"
            ],
            "success": true,
            "total_categories": 6
        }
        ```

- GET /categories/{category_id}/questions
    - General:
        - Returns a list of questions under the given category ID, success value, total number of questions under the category ID, and the current category ID.
    - Sample:
        - curl http://127.0.0.1:5000/categories/2/questions
        ```
        {
            "current_category": 1, 
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
            "total_questions": 3
        }
        ```

- GET /questions
    - General:
        - Returns a list of questions, sucess value, total number of questions, and a list of category names 
        - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    - Sample:
        - curl http://127.0.0.1:5000/questions
            ```
            {
                "categories": [
                    "Science",
                    "Art",
                    "Geography",
                    "History",
                    "Entertainment",
                    "Sports"
                ],
                "current_category": null,
                "questions": [
                    {
                        "answer": "Maya Angelou",
                        "category": 4,
                        "difficulty": 2,
                        "id": 5,
                        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                    },
                    {
                        "answer": "Muhammad Ali",
                        "category": 4,
                        "difficulty": 1,
                        "id": 9,
                        "question": "What boxer's original name is Cassius Clay?"
                    },
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
                        "answer": "Edward Scissorhands",
                        "category": 5,
                        "difficulty": 3,
                        "id": 6,
                        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
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
                "total_questions": 41
            }
            ```

- POST /questions
    - General:
        - Creates a new question using the submitted question, difficulty, answer and category. Returns the success value. 
    - Sample:
        - curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is 1 + 1?", "answer":"2", "difficulty":"1", "category":"0"}'
            ```
            {
                "success": true
            }
            ```

- DELETE /questions/{question_id}
    - General:
        - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, the new total number of questions, and the list of questions based on current page number
    - Sample:
        - curl http://127.0.0.1:5000/questions/60 -X DELETE 
        ```
        {
            "deleted": 60, 
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
                "total_questions": 21
        }
        '''

    
- POST /searchQuestions
    - General:
        - Get questions based on the search term. 
        - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
        - Returns a list of questions, total number of questions that match the search term, and the success value. 
    - Sample:
        - curl http://127.0.0.1:5000/searchQuestions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'
        ```
        {
            "current_category": null, 
            "questions": [
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
                }
            ], 
            "success": true, 
            "total_questions": 2
        }
        ```

- POST /quizzes
    - General:
        - Get questions based on the search term. 
        - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
        - Returns the next question within the given category that is not one of the previous questions, if any exists, and the success value. 
         
    - Sample:
        - curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous-questions":[], "quiz_category":{"type":"click", "id":0}}'
        ```
        {
            "question": {
                "answer": "George Washington Carver", 
                "category": 4, 
                "difficulty": 2, 
                "id": 12, 
                "question": "Who invented Peanut Butter?"
            }, 
            "success": true
        }
        ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
