from flask import Flask, render_template, session, request, jsonify
from markupsafe import escape
from boggle import Boggle
import json


app = Flask(__name__);

response_result ="";
nplays = 0;
game_score = 0;

app.config['SECRET_KEY'] = 'sshhh its a secret!!'
boggle_board = Boggle();



@app.route('/')
def index():
    """Renders the new board and starts the timer."""
    
    board = boggle_board.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0);
    nplays = 0;
    game_score = 0;
    return render_template('board_page.html', board= board, response=response_result)

@app.route('/checking_guess/', methods=['POST'])
def checking_guess():
    """Checks the word's presence and correctness and gives the score"""
    data = request.json
    board = session['board']
    
    result = boggle_board.check_valid_word(board, data["guess_word"])
    curr_score = data["score"]
 
    response_result = result
    highscore = session.get("highscore", 0);

    if result == "ok":
        if curr_score:
            curr_score = json.loads(curr_score)["score"]
            curr_score += len(data["guess_word"])
           
        else:
            curr_score = len(data["guess_word"])

        nplays = nplays + 1;
        session['highscore'] = max(curr_score, highscore)
        game_score = curr_score;
       
        return jsonify({'result': result, 'score': curr_score, 'highscore': highscore
        })

    return jsonify({'result': result})


@app.route('/endgame/', methods=['POST'])
def endgame():
    """Send response for the ajax request with nplays n score"""
    return jsonify({'nplays':nplays, 'score': game_score})
