import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

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
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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
    JSON objects includes error's status code 405 (int)
    and a message to the user (string)
    """
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "Method Not Allowed"
      }), 405
  
  
  return app

    