from pprint import pprint

from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I_Have_No_Secrets'
boggle_game = Boggle()


@app.route('/')
def home():
    """
    Show the main page  of the game and start a new game
    :return: Template, home.index
    """
    session['board'] = boggle_game.make_board()
    session['guesses'] = []
    session['score'] = 0
    session['hints'] = find_hints(session['board'])
    if 'times_played' not in session:
        session['times_played'] = 0
    if 'high_score' not in session:
        session['high_score'] = 0

    return render_template('index.html')


@app.route('/guess', methods=['POST'])
def check_guess():
    """
    Check a guess against the board
    :return: json, {result: ok} {result: not-word} {result: not-on-board}
    """
    guess = request.form.get('guess')

    result = boggle_game.check_valid_word(session['board'], guess)
    if result == 'ok':
        if guess not in session['guesses']:
            guesses = session['guesses']
            guesses.append(guess)
            session['guesses'] = guesses

            return jsonify({'result': result})
        else:
            # this was already guessed
            return jsonify({'result': 'already-guessed'})

    return jsonify({'result': result})


@app.route('/end', methods=['POST'])
def end_game():
    """
    End the game record times played and highest score
    :return:
    """
    session['times_played'] += 1
    high_score = max(request.json.get('score', 0), session['high_score'])
    session['high_score'] = max(request.json.get('score', 0), session['high_score'])

    return 'ok'


def find_hints(board, length=0, word_count=10):
    """
    Get a list of 10 words on the board
    :param board: list(list), board as saved in session
    :param length: int, minimal length of words
    :param word_count: int, number of words to find
    :return: list(str), list of found words
    """
    found_words = []
    for word in boggle_game.words:
        if boggle_game.find(board, word.upper()) and word.upper() not in found_words:
            if length == 0:
                found_words.append(word)
            elif len(word) >= length:
                found_words.append(word)
        if len(found_words) == word_count:
            break
    return found_words
# @app.route('/hint')
# def get_hint():
#     found_words = []
#     for word in boggle_game.words:
#         if boggle_game.find(TEST_BOARD, word.upper()):
#             found_words.append(word.upper())
#     print(set(found_words))
#     # result = boggle_game.check_valid_word(session['board'], guess)
#     #
#     # return jsonify(session['board'])
#
# get_hint()