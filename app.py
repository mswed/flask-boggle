from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

TEST_BOARD = [
  ["W","M","P","W","H"],
  ["N","Z","I","V","N"],
  ["I","G","C","I","Z"],
  ["W","H","B","B","L"],
  ["O","E","I","F","N"]
]

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
    session['score'] = 0
    session['hints'] = find_hints(session['board'])
    if 'times_played' not in session:
        session['times_played'] = 0
    if 'high_score' not in session:
        session['high_score'] = 0

    return render_template('index.html')


@app.route('/guess', methods=['POST'])
def check_guess():
    guess = request.form.get('guess')
    result = boggle_game.check_valid_word(session['board'], guess)

    return jsonify({'result': result})

@app.route('/end', methods=['POST'])
def end_game():
    # import pdb
    # pdb.set_trace()
    session['times_played'] += 1
    session['high_score'] = request.json.get('score', 0)

    return 'ok'

def find_hints(board):
    found_words = []
    for word in boggle_game.words:
        if boggle_game.find(board, word.upper()) and word.upper() not in found_words:
            found_words.append(word.upper())
        if len(found_words) == 11:
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