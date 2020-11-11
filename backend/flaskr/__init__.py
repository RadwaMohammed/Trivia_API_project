import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


# Constant to paginate by 10 questions per page
QUESTIONS_PER_PAGE = 10

'''
Helper function
pagination
'''
def paginate_questions(request, selection):
  """
  Paginate questions
  each page contains (QUESTIONS_PER_PAGE)

  Parameters:
  ----------
  request: dict
    the rquest object
  selection: list
    list of all questions dict 

  Returns:
  -------
  current_questions: list
    list of current questions dict per page  
  """
  # Get page form request.args object (dafault value = 1 (int))
  page = request.args.get('page', 1, type=int)
  # start idex
  start = (page - 1) * QUESTIONS_PER_PAGE
  # End index
  end = start + QUESTIONS_PER_PAGE
  # Format questions list
  questions = [question.format() for question in selection]
  # Current question per page 
  current_questions = questions[start:end]

  return current_questions



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. 
    Intialize Flask-CORS
    Allow '*' for origins
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})


  '''
  Using the after_request decorator to set Access-Control-Allow 
  by adding headers to the response
  '''
  @app.after_request
  def after_request(response): 
    """ Add headers to the response object """ 
    # Set Access-Control-Allow
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response



  '''
  Endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    """
    Retrieve all the categories ordered by category's id

    Returns:
    -------
    JSON object includes dict of all categories

    Raises:
    ------
    404 error if there is no categories
    """
    categories = Category.query.order_by(Category.id).all()
    # Format categories dict
    formatted_categories = {category.id: category.type for category in categories}
    # Error 404 if there is no categories
    if len(formatted_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': formatted_categories,
      'total_categories': len(categories)
    })



  '''
  Endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint return a list of questions, 
  number of total questions, current category, categories.  
  '''
  @app.route('/questions')
  def retrieve_questions():
    """ 
    Retrieve paginated questions
    
    Returns:
    -------
    JSON object includes a list of questions, number of total questions, current category, categories

    Raises:
    ------
    404 error if there is no questions
    """
    # Get all questions including pagination
    selection = Question.query.all()
    # Current questions per pag
    current_questions = paginate_questions(request, selection)

    # Get all categories
    categories = Category.query.order_by(Category.id).all()
    # Format categories dict
    formatted_categories = {category.id: category.type for category in categories}
    
    # Error 404 if there is no questions
    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': formatted_categories,
      'current_category': None
    })

  

  '''
  Endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    """ 
    Delete question by id
    
    Parameters:
    ----------
    question_id: int
      id of the question to be removed

    Returns:
    -------
    JSON object includes the id of the deleted question and total number of questions after the removal

    Raises:
    ------
    404 error if the question not found
    422 error if there is a problem in deleting the question
    """
    try:
      # Get the question with id = question_id
      question = Question.query.filter(Question.id == question_id).one_or_none()
      # Error 404 (not found) if there is no question with id = question_id
      if question is None:
        abort(404)
      # Delete the question
      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id,
        'total_questions': len(Question.query.all())
      })
    except:
      # Error 422 if there is a problem in deleting the question
      abort(422)



  '''
  Endpoint to POST a new question 
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    """ 
    Create a new question
    
    Returns:
    -------
    JSON object includes the created question's id, a list of the questions, number of total questions, categories

    Raises:
    ------
    422 error if there is a problem in creating the question
    """
    # create the body for the POST request for creating the new question
    body = request.get_json()
    new_question = body.get('question', None).strip()
    new_answer = body.get('answer', None).strip()
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    # Get all categories
    categories = Category.query.order_by(Category.id).all()
    # Format categories dict
    formatted_categories = {category.id: category.type for category in categories}

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'categories': formatted_categories,
        'total_questions': len(Question.query.all())
      })
    
    except:
      abort(422)



  '''
  Endpoint to get questions based on a search term. 
  It returns any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    """ 
    Search the questions based on a search term
    
    Returns:
    -------
    JSON object includes the questions found match the search_term

    Raises:
    ------
    404 error if there is no question found
    422 error if there is a problem in searching for the question
    """
    body = request.get_json()
    search_term = body.get('searchTerm', None).strip()

    try: 
      # list of questions that matches ther searchTerm
      selection = Question.query.filter(Question.question.ilike('%{}%'.format(search_term)))
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection.all())
      })
    
    except:
      abort(422)



  '''
  Endpoint to get questions based on category.   
  '''
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
    """ 
    Retrieve paginated questions based on categotry

    Parameters:
    ----------
    category_id: int
      id of the category
    
    Returns:
    -------
    JSON object includes a list of questions per category_id, number of total questions per category_id, current category dict

    Raises:
    ------
    404 error if there is no category or no questions
    """

    # Get the category that has id = category_id
    current_category = Category.query.filter_by(id=category_id).one_or_none()
    # Error 404 if there is no category
    if not current_category:
      abort(404)
    
    # Select all questions in the (current_category) 
    selection = Question.query.filter_by(category=category_id).all()
    # paginate questions
    current_questions = paginate_questions(request, selection)
    # Error 404 if there is no questions
    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions_per_category': len(current_questions),
      'current_category': current_category.format()
    })

  
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''


  '''
  Error handlers for all expected errors  
  '''

  '''
  Error 404 (Resource not found)
  '''
  @app.errorhandler(404)
  def not_found(error):
    """
    Function not_found handle error 404 

    Returns:
    -------
    JSON objects includes error's status code 404 (int)
    and a message to the user (string)
    """
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource Not Found"
      }), 404
  

  '''
  Error 422 (Unprocessable operation)
  '''
  @app.errorhandler(422)
  def unprocessable(error):
    """
    Function unprocessable handle error 422 

    Returns:
    -------
    JSON objects includes error's status code 422 (int)
    and a message to the user (string)
    """
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable"
      }), 422


  '''
  Error 400 (Bad request)
  '''
  @app.errorhandler(400)
  def bad_request(error):
    """
    Function bad_request handle error 400 

    Returns:
    -------
    JSON objects includes error's status code 400 (int)
    and a message to the user (string)
    """
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad Request"
      }), 400


  '''
  Error 405 (Method not allowed)
  '''
  @app.errorhandler(405)
  def not_allowed(error):
    """
    Function not_allowed handle error 405 

    Returns:
    -------
    JSON objects includes error's status code 405 (int)
    and a message to the user (string)
    """
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "Method Not Allowed"
      }), 405
  
  
  return app

    