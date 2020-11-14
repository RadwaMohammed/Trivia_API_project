# Trivia API Project

Trivia is an application where users can test and gain knowledge in different categories (science, art, geography, history, entertainment and sports).

The application contains other features:
- Display questions in different categories, and the user can choose a specific category to view questions related to it.
- Each question is displayed with its degree of difficulty, its category, and its answer.
- Add question and require that user includes question and answer text.
- Delete question.
- Search for questions based on a text query string.
- Play the quiz game, randomizing either all questions or within a specific category.


## Getting Started

Download or Clone the repository to your computer.

### Prerequisites and Local Development

You should already have Python3, pip, node, and npm installed.

### Backend

Navigate to the `/backend` directory, open your terminal and run and run:

```bash
pip install -r requirements.txt
```
This will install all of the required packages within the `requirements.txt` file.

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Running the server

From the `backend` directory, To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Frontend

Navigate to the `frontend` directory, open your terminal and run:

```bash
npm install
```
In order to run the app run:

```bash
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Ignore the dropdb command the first time you run tests.

## API Reference

### Getting Started

- Backend Base URL: http://127.0.0.1:5000/
- Frontend Base URL: http://127.0.0.1:3000/


### Endpoints

#### GET `/categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: an object with a single key, 
  - `categories`: that contains a object of id: category_string key:value pairs

```json 
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_categories": 6
}

```


#### GET `/questions`

- Fetches a dictionary of categories, the current category, a list of questions paginated by 10 questions and the total of questions
- Request Arguments:
  - `page` (integer) - the page number `/questions?page=1` default is 1
- Returns: an object with keys
  - `categories`: a dictionary of categories
  - `current_category`: the current category
  - `questions`: a list of questions (paginated by 10 items)
  - `success`: a `boolean` indication of successful response
  - `total_questions`: the total of questions

```json
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
    "total_questions": 19
}

```


### DELETE `/questions/<int:question_id>/`

- Delete a question by question's id
- Request Arguments:
  - `question_id`: (integer) id of the question to be removed
- Returns: an object with keys:
  - `deleted`: id of the deleted question
  - `success`: a `boolean` as indication of the successful removal
  - `total_questions`: total number of questions after the removal

```json
{
    "deleted": 6,
    "success": true,
    "total_questions": 18
}
```


### POST `/questions`

- Create a new question
- Request Arguments:
  - `question`: (string) - the question
  - `answer`: (string) - the answer
  - `difficulty`: (integer) - the question's difficulty
  - `category`: (integer) - the question's category
- Returns: an object with keys:
  - `categories`: a dictionary of categories
  - `created`: the created question's id
  - `questions`: a list of questions paginated by 10 questions after creating new questions 
  - `success`: a `boolean` as indication of the successful creation
  - `total_questions`: total number of questions after the creation of new question

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "created": 24,
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
    "total_questions": 20
}
```


### POST `/questions/search`

- Search questions based on a search term
- Request Arguments:
  - `searchTerm` (string) - The string term to search
- Returns: an object with keys:
  - `questions`: a list of the questions found match the searchTerm
  - `success`: a `boolean` as indication of the successful search
  - `total_questions`: The total of questions found

```json
{
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


### GET `/categories/<int:category_id>/questions`

- Fetches a list of paginated questions based on categotry
- Request Arguments:
  - `category_id` (integer): id of the category
- Returns: an object with these keys:
  - `current_category`: the current category dict
  - `questions`: a list of questions per category_id
  - `success`: a `boolean` as indication of the successful response
  - `total_questions_per_category`: total number of questions per category_id

```json
{
    "current_category": {
        "id": 6,
        "type": "Sports"
    },
    "questions": [
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
            "answer": "qqqq",
            "category": 6,
            "difficulty": 2,
            "id": 24,
            "question": "what"
        }
    ],
    "success": true,
    "total_questions": 3
}
```


### POST `/quizzes`

- Fetches random question to play the quiz
- Request arguments:
  - `quiz_category` (dictionary): the quiz category with `type` and `id` keys.
  - `previous_questions` (list of integer): list of the previous questions id
- Returns: An object with keys:
  - `success`: a `boolean` as indication of the successful response
  - `question`: the question to play
  - `total_quizzes`: total number of quizzes of the secified category

```json
{
    "question": {
        "answer": "One",
        "category": 2,
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    "success": true,
    "total_quizzes": 4
}
```


### Error Handling

Errors are returned as JSON in the following format: 

```json
{
    "success": False,
    "error": 422,
    "message": "Unprocessable"
}

```
The API will return errors:
- 404 - Resource Not Found
- 422 - Unprocessable
- 400 - Bad Request
- 405 - Method Not Allowed


### Error 404

```json
{
    "success": False, 
    "error": 404,
    "message": "Resource Not Found"
}
```

### Error 422

```json
{
    "success": False, 
    "error": 422,
    "message": "Unprocessable"
}
```

### Error 400

```json
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```

### Error 405

```json
{
    "success": False, 
    "error": 405,
    "message": "Method Not Allowed"
}
```

