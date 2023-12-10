from pprint import pprint

from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I_Have_No_Secrets'
boggle_game = Boggle()
DEBUG = False


@app.route('/')
def home():
    """
    Show the main page  of the game and start a new game
    :return: Template, home.index
    """
    session['board'] = boggle_game.make_board()

    session['tries'] = []
    session['score'] = 0
    if 'times_played' not in session:
        session['times_played'] = 0
    if 'high_score' not in session:
        session['high_score'] = 0

    session['wob_locations'] = find_hints(session['board'])
    session['words_on_board'] = [w[0] for w in session['wob_locations']]

    if DEBUG:
        session['hints'] = find_hints(session['board'])
    else:
        session['hints'] = []

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
        if guess not in session['tries']:
            # This is the first time we're guessing this word add it to the tries list
            tries = session['tries']
            tries.append(guess)
            session['tries'] = tries
            hint_index = session['words_on_board'].index(guess)
            session['words_on_board'].pop(hint_index)
            session['wob_locations'].pop(hint_index)

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
    game_result = {'score': request.json.get('score', 0), 'timesPlayed': session['times_played']}

    original_high_score = session['high_score']
    session['high_score'] = max(int(request.json.get('score', 0)), session['high_score'])
    if original_high_score != session['high_score']:
        game_result['highScore'] = session['high_score']

    return jsonify(game_result)


def find_hints(board, length=0, word_count=0):
    """
    Get a list of 10 words on the board
    :param board: list(list), board as saved in session
    :param length: int, minimal length of words
    :param word_count: int, number of words to find
    :return: list(str), list of found words
    """
    found_words = []
    for word in boggle_game.words:
        found = boggle_game.find(board, word.upper())
        if found and word.upper() not in found_words:
            indexes = found[1:]
            if length == 0:
                found_words.append((word, indexes))
            elif len(word) >= length:
                found_words.append((word, indexes))

        if word_count == 0:
            # find all words
            continue
        if len(found_words) == word_count:
            break
    return found_words


@app.route('/hint')
def get_hint():
    try:
        hints = session['wob_locations']
        hint = hints[-1]

        return jsonify(hint)
    except IndexError:
        print('Ooops, could not find a hint')
