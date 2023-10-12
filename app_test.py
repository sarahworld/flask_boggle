
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.testing = True
      


    def test_homepage(self):
        print("In here")
        with app.test_request_context():
      
            response = self.client.get('/')
            html = response.get_data(as_text=True)

            self.assertIn('<h1>Boggle Game</h1>', html)
            self.assertIsNone(session.get('highscore'))


    def test_valid_word(self):
        with app.test_request_context():
            with self.client as client:
                with client.session_transaction() as sess:
                    session["board"] = [["B", "A", "T", "T", "T"], 
                                    ["B", "A", "T", "T", "T"], 
                                    ["B", "A", "T", "T", "T"], 
                                    ["B", "A", "T", "T", "T"], 
                                    ["B", "A", "T", "T", "T"]]
                    data = {
                        'guess_word':'cat'
                    }
                    response = self.client.post('/checking_guess/', data)
                    self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        data = {
            'guess_word':'impossible'
        }
        response = self.client.post('/checking_guess/', data)
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_english_word(self):
        data = {
            'guess_word':'adfdgvfbsfbtgfrfbrs'
        }
        response = self.client.post('/checking_guess/', data)
        self.assertEqual(response.json['result'], 'not-word')
    
        



