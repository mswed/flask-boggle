from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def test_homepage(self):
        with app.test_client() as client:
            result = client.get('/')
            html = result.get_data(as_text=True)

            self.assertEqual(result.status_code, 200)
            self.assertIn('<h1>BOGGLE!</h1>', html)

    def test_check_guess(self):
        """
        Test for handling words found on the board, valid words and not valid words
        """
        # Initialize a game
        game = Boggle()

        with app.test_client() as client:
            # Start a game
            client.get('/')

            # Search for all possible words on the board
            found_words = []
            for word in game.words:
                if game.find(session['board'], word):
                    found_words.append(word.upper())
            test_words = list((set(found_words)))[0:3]

            # Test 3 words we found to make sure we get the correct OK response
            for word in test_words:
                result = client.post('/guess', data={'guess': word})
                self.assertTrue(result.json)
                self.assertEqual(result.json, {'result': 'ok'})

            # Search for a valid word that is not on the board
            not_on_board = None
            while not_on_board is None:
                word = game.words.pop()
                if word not in found_words:
                    not_on_board = word

            # Test the word to see that we get the correct not-on-board response
            result = client.post('/guess', data={'guess': not_on_board})
            self.assertTrue(result.json)
            self.assertEqual(result.json, {'result': 'not-on-board'})

            # Test a non-existing word to make sure we get the correct not-word response
            result = client.post('/guess', data={'guess': 'rlkewjrlkweanag'})
            self.assertTrue(result.json)
            self.assertEqual(result.json, {'result': 'not-word'})


