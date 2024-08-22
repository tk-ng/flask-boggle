from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn('Score:', html)
            self.assertIn('Game:', html)
            self.assertIn('Highest Score:', html)

    def test_validate_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["G","S","B","C","K"],["E","H","K","C","S"],["N","D","Q","O","S"],["S","Z","H","D","T"],["W","J","E","F","G"]]
            
            res = client.post('/validate',json={'guess':'hot'})
            self.assertEqual(res.json["result"],'ok')

    def test_invalid_word(self):
        with app.test_client() as client:
            client.get('/')
            res = client.post('/validate',json={'guess':'invalid'})
            self.assertEqual(res.json["result"],'not-on-board')

    def test_non_english_word(self):
        with app.test_client() as client:
            client.get('/')
            res = client.post('/validate',json={'guess':'oshoiwer'})
            self.assertEqual(res.json["result"],'not-word')

    def test_gameover(self):
        with app.test_client() as client:
            res = client.post('/gameover',json={'score':'15'})
            self.assertEqual(res.json["highest_score"], 15)