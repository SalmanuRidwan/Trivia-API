import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import TEST_DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, 'localhost:5432', self.database_name)
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

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('categories'))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('categories'))

    def test_404_test_on_request_greathan_valid_page(self):
        res = self.client().get('/questions?page=77')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'resource not found')
    
    def test_delete_question(self):
        question_id = Question.query.first().format()['id']
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        question = Question.query.filter_by(id = question_id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)
        self.assertEqual(data.get('success'), True)    
        
    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'Very hungry'})
        data = json.loads(res.data)
        term = data.get('questions')
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertEqual(len(term), 0)
        
    def test_category_based_question(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)

    def test_get_question(self):
        res = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"id": 1, "type": "Science"}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(data.get('question'), dict))
        
    def test_404_requesting_category(self):
        res = self.client().get('/categories/4')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data.get('message'), 'resource not found')
        
    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1065')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'resource not found')
        
    def test_405_on_search_question(self):
        res = self.client().get('/questions/98')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data.get('success'), False)
        
    def test_404_on_unknown_category_question(self):
        res = self.client().get('/categories/9888884/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'resource not found')
    
    def test_404_on_getting_question_with_no_input(self):
        res = self.client().get('/quizzes/3')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'resource not found')
    
    
    def test_create_new_question(self):
        res = self.client().post('/questions', json={"new_question": "There are how many days in a week?", "new_answer": 7, "new_category": 3, "new_difficulty": 1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        
    def test_405_on_add_new_questions(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data.get('success'), False)
    
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()