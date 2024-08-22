from boggle import Boggle
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "a_secret_key"
app.debug = True

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def show_board():
    board = boggle_game.make_board()
    session['board'] = board
    highest_score = session.get("highest_score", 0)
    nplays = session.get("nplays", 0)
    return render_template('index.html', board=board, highest_score=highest_score,
                           nplays=nplays)

@app.route('/validate', methods=["POST"])
def validate_word():
    data = request.json
    word = data.get("guess")
    validity = boggle_game.check_valid_word(session['board'],word)
    result = {"result":validity}
    return jsonify(result)

@app.route('/gameover', methods=["POST"])
def get_final_score():
    data = request.json
    score = int(data.get("score"))
    highest_score = session.get('highest_score',0)
    if score > highest_score:
        session["highest_score"] = score

    session['nplays'] = session.get('nplays', 0) + 1
    return {"highest_score":session.get('highest_score',0),"count":session['nplays']}