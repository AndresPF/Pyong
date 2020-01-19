import os
from flask import Flask, request, jsonify, abort, redirect
from models import setup_db, Player, Match
from flask_cors import CORS
from auth import AuthError, requires_auth
from datetime import datetime
import pytz

MATCHES_PER_PAGE = 10

def paginate_matches(request, selection):
	page = request.args.get('page', 1, type=int)
	start =  (page - 1) * MATCHES_PER_PAGE
	end = start + MATCHES_PER_PAGE

	matches = [match.format() for match in selection]
	current_matches = matches[start:end]

	return current_matches

def create_app(test_config=None):

	app = Flask(__name__)
	setup_db(app)
	cors = CORS(app, resources={r"*": {"origins": "*"}})

	# CORS Headers 
	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
		response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE')
		return response

	@app.route('/')
	def get_greeting():
		excited = os.environ['EXCITED']
		greeting = "Hello" 
		if excited == 'true': greeting = greeting + "!!!!!"
		return greeting

	@app.route('/login')
	def login():
		link = 'https://' + os.environ['AUTH0_DOMAIN']
		link += '/authorize?'
		link += 'audience=' + os.environ['API_AUDIENCE'] + '&'
		link += 'response_type=token&'
		link += 'client_id=' + os.environ['CLIENT_ID'] + '&'
		link += 'redirect_uri=' + os.environ['CALLBACK_URL']
		return redirect(link, code=302)

	@app.route('/callback')
	def login_callback():
		print(request.url)
		return 'login callback page'

	@app.route('/players', methods=['GET'])
	@requires_auth('get:player')
	def get_players(payload):
		selection = Player.query.order_by(Player.id).all()

		if len(selection) == 0:
			abort(404)

		formatted_players = [player.format() for player in selection]

		return jsonify({
			'success': True,
			'players': formatted_players
		})

	@app.route('/players', methods=['POST'])
	@requires_auth('post:player')
	def create_player(payload):
		body = request.get_json()

		new_name = body.get('name', None)
		new_email = body.get('email', None)

		try:
			player = Player(name=new_name, email=new_email)
			player.insert()

			return jsonify({
				'success': True,
				'created': player.id
			})

		except:
			abort(422)

	@app.route('/matches', methods=['GET'])
	@requires_auth('get:match')
	def get_matches(payload):
		selection = Match.query.order_by(Match.id).all()
		current_matches = paginate_matches(request, selection)

		if len(current_matches) == 0:
			abort(404)

		return jsonify({
			'success': True,
			'matches': current_matches,
		})

	@app.route('/matches', methods=['POST'])
	@requires_auth('post:match')
	def create_match(payload):
		body = request.get_json()

		new_scoreA = body.get('scoreA', None)
		new_scoreB = body.get('scoreB', None)
		new_date = datetime.now().astimezone(pytz.UTC)
		new_playerA_id = body.get('playerA', None)
		new_playerB_id = body.get('playerB', None)

		try:
			match = Match(scoreA=new_scoreA, scoreB=new_scoreB, date=new_date, playerA_id=new_playerA_id, playerB_id=new_playerB_id)
			match.insert()

			return jsonify({
				'success': True,
				'created': match.id,
				'date': match.date
			})

		except:
			abort(422)

	@app.route('/matches/<int:match_id>', methods=['PATCH'])
	@requires_auth('patch:match')
	def update_match(payload, match_id):
		body = request.get_json()
		match = Match.query.get(match_id)

		if match is None:
			abort(404)

		new_scoreA = body.get('scoreA', None)
		new_scoreB = body.get('scoreB', None)

		if new_scoreA is None and new_scoreB is None:
			abort(422)

		try:
			if new_scoreA is not None:
				match.scoreA = new_scoreA

			if new_scoreB is not None:
				match.scoreB = new_scoreB

			match.update()

			return jsonify({
				'success': True,
				'match': match.format()
			})

		except:
			abort(422)

	@app.route('/matches/<int:match_id>', methods=['DELETE'])
	@requires_auth('delete:match')
	def delete_match(payload, match_id):
		match = Match.query.get(match_id)

		if match is None:
			abort(404)

		try:
			match.delete()

			return jsonify({
				'success': True,
				'delete': match_id
			})

		except:
			abort(422)

	## Error Handling

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({
			"success": False, 
			"error": 422,
			"message": "unprocessable"
		}), 422


	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			"success": False,
			"error": 404,
			"message": "resource not found"
			}), 404


	@app.errorhandler(AuthError)
	def unauthorized(err):
		return jsonify({
			"success": False,
			"error": err.status_code,
			"message": err.error
			}), err.status_code

	return app

app = create_app()

if __name__ == '__main__':
	app.run()