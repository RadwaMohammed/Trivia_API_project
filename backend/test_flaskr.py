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
        """ Test for retrieve_questions"""
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
        """ Test for sending 404 error if requesting beyond valid page"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        # status code = 404
        self.assertEqual(res.status_code, 404)
        # success = False
        self.assertEqual(data['success'], False)
        # massage = 'Resource Not Found'
        self.assertEqual(data['message'], 'Resource Not Found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()