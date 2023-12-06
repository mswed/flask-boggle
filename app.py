from flask import Flask, render_template, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I_Hhave_No_Secrets'
boggle_game = Boggle()


@app.route('/')
def home():
    session['board'] = boggle_game.make_board()

    return render_template('index.html')
