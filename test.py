import unittest
from app import app
from flask import session
from boggle import Boggle
from datetime import datetime, timedelta
import json


class FlaskTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.boggle_game = Boggle()

    def test_home(self):
        with self.app.session_transaction() as session:
            session['data'] = '[["Y", "Y", "Z", "I", "H"], ["Y", "H", "C", "N", "G"], ["G", "V", "S", "S", "M"], ["F", "N", "B", "U", "I"], ["P", "M", "J", "X", "V"]]'
            session['end-time'] = str((datetime.now() +
                                       timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'))
            session['score'] = '0'
        session['found-words'] = '[]'
        response = self.app.get()

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Home</title>", response.data)

    def test_game_get(self):

        with self.app.session_transaction() as session:
            session['data'] = '[["Y", "Y", "Z", "I", "H"], ["Y", "H", "C", "N", "G"], ["G", "V", "S", "S", "M"], ["F", "N", "B", "U", "I"], ["P", "M", "J", "X", "V"]]'
            end_time = str((datetime.now() +
                            timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'))
            session['end-time'] = end_time
            session['score'] = '0'
            session['found-words'] = '[]'

        response = self.app.get('/game')
        self.assertEqual({"board": json.loads(
            '[["Y", "Y", "Z", "I", "H"], ["Y", "H", "C", "N", "G"], ["G", "V", "S", "S", "M"], ["F", "N", "B", "U", "I"], ["P", "M", "J", "X", "V"]]'),
            "endTime": end_time,
            "score": '0'},
            json.loads(response.data)
        )

    def test_game_post(self):

        with self.app.session_transaction() as session:
            session['data'] = '[["Y", "Y", "Z", "I", "H"], ["Y", "H", "C", "N", "G"], ["G", "V", "S", "S", "M"], ["F", "N", "B", "U", "I"], ["P", "M", "J", "X", "V"]]'
            session['end-time'] = str((datetime.now() +
                                       timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'))
            session['score'] = '0'
            session['found-words'] = '[]'

        # Test valid word
        response = self.app.post('/game', json={'word': 'bus'})
        self.assertEqual(b'ok', response.data)

        # Test invalid word
        response = self.app.post('/game', json={'word': 'fnbui'})
        self.assertNotEqual(b'ok', response.data)

        # Test valid word that doesn't exist
        response = self.app.post('/game', json={'word': 'apple'})
        self.assertNotEqual(b'ok', response.data)

        with self.app.session_transaction() as session:
            session['data'] = '[["Y", "Y", "Z", "I", "H"], ["Y", "H", "C", "N", "G"], ["G", "V", "S", "S", "M"], ["F", "N", "B", "U", "I"], ["P", "M", "J", "X", "V"]]'
            session['end-time'] = str((datetime.now() -
                                       timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'))  # Set time to the past to simulate a timed-out game
            session['score'] = '0'
            session['found-words'] = '[]'

            # Test valid word after timed out
        response = self.app.post('/game', json={'word': 'zinc'})
        self.assertEqual(
            b"can't add anymore words, game is already over", response.data)


if __name__ == '__main__':
    unittest.main()
