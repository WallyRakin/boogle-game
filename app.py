from flask import Flask, session, render_template, jsonify, request
from datetime import datetime, timedelta
from boggle import Boggle
import json

boggle_game = Boggle()
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route("/")
def home():
    # creates a new session if a valid session is not already available
    if not (session.get('data') and session.get('end-time') and session.get('found-words') and session.get('score')) or (datetime.now() > datetime.strptime(session.get('end-time'), "%Y-%m-%d %H:%M:%S")):
        board = boggle_game.make_board()
        session['data'] = json.dumps(board)
        session['end-time'] = ((datetime.now() +
                                timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'))
        session['found-words'] = '[]'
        session['score'] = '0'
        # print(json.dumps(board))
    else:
        board = json.loads(session.get('data'))
    found_words = json.loads(session.get('found-words'))
    return render_template('home.html', board=board, row=range(len(board)), col=range(len(board[0])), data=json.dumps(board), found_words=found_words)


@app.route("/game", methods=['GET', 'POST'])
def game():

    if request.method == 'GET':
        return jsonify({"board": json.loads(session.get('data')), "endTime": session.get('end-time'), "score": session.get('score')})
    elif request.method == 'POST':
        data = request.get_json()
        word = data.get("word")
        result = boggle_game.check_valid_word(
            json.loads(session.get('data')), word)

        found_words = json.loads(session.get('found-words'))
        # print(found_words)

        if datetime.now() > datetime.strptime(session.get('end-time'), "%Y-%m-%d %H:%M:%S"):
            # escapes function if the game is already over
            return "can't add anymore words, game is already over"

        if word in found_words:
            # escapes function if word is a duplicate
            return 'word has already been selected'

        score = int(session.get('score'))

        if result == 'ok':
            score += 100
        elif result == 'not-on-board':
            return result
        else:
            return result

        found_words.append(word)
        session['found-words'] = json.dumps(found_words)
        session['score'] = score

    return result


# Ensure this is set to True or not set at all
# app.run(debug=True)
