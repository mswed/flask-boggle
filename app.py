from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I_Hhave_No_Secrets'
boggle_game = Boggle()


@app.route('/')
def home():
    session['board'] = boggle_game.make_board()
    print(session['board'])

    return render_template('index.html')


@app.route('/guess', methods=['POST'])
def check_guess():
    guess = request.form.get('guess')
    result = boggle_game.check_valid_word(session['board'], guess)

    return jsonify({'result': result})
    # if guess in boggle_game.words:
    #     print('Found word!', guess)
    # else:
    #     print('No such word in DB', guess)
    #
    # print(boggle_game.check_valid_word(session['board'], guess))
    # return 'WHAT?'
