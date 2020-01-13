import os
from flask import Flask
from models import setup_db
from flask_cors import CORS
from auth import AuthError, requires_auth

def create_app(test_config=None):

	app = Flask(__name__)
	setup_db(app)
	cors = CORS(app, resources={r"*": {"origins": "*"}})

	# CORS Headers 
	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
		response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
		return response

	@app.route('/')
	def get_greeting():
		excited = os.environ['EXCITED']
		greeting = "Hello" 
		if excited == 'true': greeting = greeting + "!!!!!"
		return greeting

	@app.route('/players')
	def get_players():
		return "Be cool, man, be coooool! You're almost a FSND grad!"

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
			}), 401

	return app

app = create_app()

if __name__ == '__main__':
	app.run()