import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'passR00','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # question for testing    
        self.new_question = {
            'question': 'Which is the tallest mountain in the world?',
            'answer': 'Mount Everest',
            'category': 3,
            'difficulty': 2
        }

        self.new_question_not_valid = {
            'question': 'Which is the tallest mountain in the world?',
            'answer': 'Mount Everest',
            'category': 'Geography', # string to make it not valid question
            'difficulty': 2
        }  

        # request data for test
        self.request_body_data = {
            'previous_questions': [16, 19],
            'quiz_category': {
                'type': 'Art', 
                'id': 2
                }
        }   

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    '''
    Test for categories
    '''
    def test_retrieve_categories(self):
        """ Test for retrieve_categories"""
        res = self.client().get('/categories')
        # Load the data
        data = json.loads(res.data)

        # status code = 200 
        self.assertEqual(res.status_code, 200)
        # success = True
        self.assertEqual(data['success'], True)
        # categories is a dict type
        self.assertIsInstance(data['categories'], dict)
        # categories dict not empty
        self.assertTrue(len(data['categories']))
    


    '''
    Test for questions
    '''
    def test_get_paginated_questions(self):
        """ Test for retrieve_questions """
        res = self.client().get('/questions')
        # Load the data
        data = json.loads(res.data)

        # status code = 200  
        self.assertEqual(res.status_code, 200)
        # success = True
        self.assertEqual(data['success'], True)
        # questions list is exist
        self.assertTrue(data['questions'])
        # questions is a list type
        self.assertIsInstance(data['questions'], list)
        # question list not empty
        self.assertTrue(len(data['questions']))
        # categories dict is exist
        self.assertTrue(data['categories'])
    

    def test_404_sent_requesting_beyond_valid_page(self):
        """ Test for sending 404 error if requesting beyond valid page """
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        # status code = 404
        self.assertEqual(res.status_code, 404)
        # success = False
        self.assertEqual(data['success'], False)
        # massage = 'Resource Not Found'
        self.assertEqual(data['message'], 'Resource Not Found')



    '''
    Test for delete a question
    '''
    def test_delete_question(self):
        """ Test for delete_question """
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)
        # Get the question from the database
        question = Question.query.filter(Question.id == 12).one_or_none()

        # status code = 200 
        self.assertEqual(res.status_code, 200)
        # success = True
        self.assertEqual(data['success'], True)
        # check the id of the deleted question
        self.assertEqual(data['deleted'], 12)
        # total_quetions is not empty
        self.assertTrue(data['total_questions'])
        # check that question is deleted
        self.assertEqual(question, None)
        

    def test_422_if_delete_question_fails(self):
        """ Test for 422 error if the question not exist """
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        # status code = 422
        self.assertEqual(res.status_code, 422)
        # success = False
        self.assertEqual(data['success'], False)
        # message = 'Unprocessable'
        self.assertEqual(data['message'], 'Unprocessable')



    '''
    Test for create a new question
    '''
    def test_create_new_question(self):
        """ Test for create_question """
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        # status code = 200 
        self.assertEqual(res.status_code, 200)
        # success = True
        self.assertEqual(data['success'], True)
        # check that question is created
        self.assertIsNotNone(data['created'])
        self.assertTrue(len(data['questions']))


    def test_422_if_create_question_fails(self):
        """ Test for 422 error if the question creation failed """
        res = self.client().post('/questions', json=self.new_question_not_valid)
        data = json.loads(res.data)

        # status code = 422
        self.assertEqual(res.status_code, 422)
        # success = False
        self.assertEqual(data['success'], False)
        # message = 'Unprocessable'
        self.assertEqual(data['message'], 'Unprocessable')
    

    def test_405_if_question_creation_not_allowed(self):
        """ Test for 405 error if the the end point is wrong """
        res = self.client().post('/questions/55', json=self.new_question)
        data = json.loads(res.data)
        
        # status code = 405
        self.assertEqual(res.status_code, 405)
        # success = False
        self.assertEqual(data['success'], False)
        # message = 'Method Not Allowed'
        self.assertEqual(data['message'], 'Method Not Allowed')


    '''
    Test for search questions by searchTerm
    '''
    def test_get_question_search_with_results(self):
        """ Test for get question search with result """
        # here we want to search 'title' through the questions
        res = self.client().post('/questions/search', json={'searchTerm': 'title'})
        # got the data
        data = json.loads(res.data)

        # status code = 200 
        self.assertEqual(res.status_code, 200)
        # success = True
        self.assertEqual(data['success'], True)
        # check questions is exist
        self.assertTrue(data['total_questions'])
        # check we have 2 question contain 'title'
        self.assertEqual(len(data['questions']), 2)


    def test_get_question_search_without_results(self):
        """ Test for question search without results """
        # search for somthing not in the database
        res = self.client().post('/questions/search', json={'searchTerm': 'rrrrrr'})
        data = json.loads(res.data)

        # status code = 200
        self.assertEqual(res.status_code, 200)
        # success = True
        self.assertEqual(data['success'], True)
        # check total questions list is empty
        self.assertEqual(data['total_questions'], 0)
        # check current questions list is empty
        self.assertEqual(len(data['questions']), 0)


    '''
    Test for get questions by category's id
    '''
    def test_get_questions_by_category_id(self):
        """ Test for questions filtered by category's id """
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        # status code = 200
        self.assertEqual(res.status_code, 200)
        # success = True
        self.assertEqual(data['success'], True)
        # check current_category's id is the id in the endpoint
        self.assertEqual(data['current_category']['id'], 6)
        # check total questions per category's with id = 6 are two questions
        self.assertEqual(data['total_questions_per_category'], 2)


    def test_404_not_found_if_category_invalid(self):
        """ Test for 404 error if the category's id is invalid """
        res = self.client().get('/categories/3000/questions')
        data = json.loads(res.data)

        # status code = 404
        self.assertEqual(res.status_code, 404)
        # success = False
        self.assertEqual(data['success'], False)
        # massage = 'Resource Not Found'
        self.assertEqual(data['message'], 'Resource Not Found')



    '''
    Test for qet question to play quiz
    '''
    def test_play_random_quiz(self):
        """ Test for get random question to play quiz """
        res = self.client().post('/quizzes', json=self.request_body_data)
        data = json.loads(res.data)

        # status code = 200 
        self.assertEqual(res.status_code, 200)
        # success = True
        self.assertEqual(data['success'], True)
        # check there is a question
        self.assertTrue(data['question'])
        # question is in the correct category
        self.assertEqual(data['question']['category'], 2)
        # check previous question not accepted
        self.assertNotEqual(data['question']['id'], 16)


    def test_422_error_play_quiz_without_data(self):
        """ Test for 422 error request with no data to play quiz """
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        # status code = 422
        self.assertEqual(res.status_code, 422)
        # success = False
        self.assertEqual(data['success'], False)
        # message = 'Unprocessable'
        self.assertEqual(data['message'], 'Unprocessable')

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()