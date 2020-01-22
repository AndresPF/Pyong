import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from app import create_app
from models import setup_db, Player, Match, db_drop_and_create_all


class PyongTestCase(unittest.TestCase):
    """This class represents the pyong test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
        self.player_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUVTVPRUU1TnpreFFrRkdNa1F4TTBFeE1UWTJNVVpCUkRjeE1qTXdSRUV5UmpRMk5qWkVOdyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYXBmLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMDc5MjExNTE0ODM0NTM1MTUzNCIsImF1ZCI6WyJweW9uZyIsImh0dHBzOi8vZnNuZC1hcGYuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU3OTY1NTc4OSwiZXhwIjoxNTc5NzQyMTg5LCJhenAiOiJDWldQeGNVUkNLVTNBMU9UZDZLRkhJNzh2b0hKcFBoZiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6bWF0Y2giLCJnZXQ6cGxheWVyIiwicG9zdDptYXRjaCIsInBvc3Q6cGxheWVyIl19.U4EPhP-5maqrnYSYctZJx7Bh_hLirTNWVT5l4SMTpdpRtZku5nNG8p9g8-G7MKnp13hHBZ_Yecg6ac52RMYQGx3P0hH1a2PDSg-2Kxfl6kmPJW-9L0ZJmq8KBrUOWsw52_nL6RTzV4CDW-dItnxTICvkjl3_S_LCIpFWdkpJUiBmI7eSgqIBGCqXjaE-o8DGdIrI4jyAe_ynkL4VhBk5wdX6vwtPN0I1-ip3XGkcVS3ZPLkEu75gSGLMTCW3K_lSBQzj-XoPgdLMZRcndjQtu82u3-mkmPzJjqiCUeCBgVM-1gAf1EPWid_XqrDsb5o8ZYyDwKBK1kIMZjR8D5R-Mw'
        self.admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUVTVPRUU1TnpreFFrRkdNa1F4TTBFeE1UWTJNVVpCUkRjeE1qTXdSRUV5UmpRMk5qWkVOdyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYXBmLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNzcwODg1MDE1MjE1MTM5NDAzNSIsImF1ZCI6WyJweW9uZyIsImh0dHBzOi8vZnNuZC1hcGYuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU3OTY1NjA1OCwiZXhwIjoxNTc5NzQyNDU4LCJhenAiOiJDWldQeGNVUkNLVTNBMU9UZDZLRkhJNzh2b0hKcFBoZiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6bWF0Y2giLCJkZWxldGU6cGxheWVyIiwiZ2V0Om1hdGNoIiwiZ2V0OnBsYXllciIsInBhdGNoOm1hdGNoIiwicG9zdDptYXRjaCIsInBvc3Q6cGxheWVyIl19.RjcNkfBYnsYm1xwue6HcdCu4V6KaD7OGdOe5NUIb2C39c0_aXFmmTOoKAF1RKzOkv6yVnLlWyfKnF1nrry-JDngzzJgOe9qFw_QlVJ3aOR_MuLNYtnbNv3eZW5I3cgEWNuw0RqOcwEW4EVSfVic4tySWtCmJqDKyBOktVKQ2_KJnrBFa8MVst300sD6agW4flt-tMYtv6PvM4mT8AvDkECTN4Pt6x943McWeZzdIq4zSEU_pc-wDLUC_KFcBHUHdax_-ev6Mpb6dn8DzWkhsJ3yViKbeRBmldwmLT7AIYpPPHa_N0ewj1lMzeY0i6N1rRcj8w5eOvNUYfThUk79hNQ'
        self.new_player = {
            'name': 'Tester3',
            'email': 'tester3@test.com'
        }
        self.new_match = {
            'scoreA': 2,
            'scoreB': 1,
            'playerA': 1,
            'playerB': 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_players(self):
        res = self.client().get(
            '/players',
            headers=dict(
                Authorization='Bearer ' + self.player_token
            )
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players'])
        self.assertTrue(len(data['players']))

    def test_401_get_players_no_token(self):
        res = self.client().get('/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(len(data['message']))

    def test_create_player(self):
        res = self.client().post(
            '/players',
            headers=dict(
                Authorization='Bearer ' + self.player_token
            ),
            json=self.new_player,
            content_type='application/json'
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_401_create_player_no_token(self):
        res = self.client().post('/players', json=self.new_player)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(len(data['message']))

    def test_get_paginated_matches(self):
        res = self.client().get(
            '/matches',
            headers=dict(
                Authorization='Bearer ' + self.player_token
            )
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['matches'])
        self.assertTrue(len(data['matches']))

    def test_404_paginated_matches_beyond_page(self):
        res = self.client().get(
            '/matches?page=1000',
            headers=dict(
                Authorization='Bearer ' + self.player_token
            )
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(len(data['message']))

    def test_create_match(self):
        res = self.client().post(
            '/matches',
            headers=dict(
                Authorization='Bearer ' + self.player_token
            ),
            json=self.new_match,
            content_type='application/json'
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_401_create_match_no_token(self):
        res = self.client().post('/matches', json=self.new_match)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(len(data['message']))

    def test_patch_match(self):
        res = self.client().patch(
            '/matches/1',
            headers=dict(
                Authorization='Bearer ' + self.admin_token
            ),
            json={
                "scoreA": 5,
                "scoreB": 4
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['match'])

    def test_403_patch_match_incorrect_permission(self):
        res = self.client().patch(
            '/matches/2',
            headers=dict(
                Authorization='Bearer ' + self.player_token
            ),
            json={
                "scoreA": 5,
                "scoreB": 4
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(len(data['message']))

    def test_delete_match(self):
        res = self.client().delete(
            '/matches/2',
            headers=dict(
                Authorization='Bearer ' + self.admin_token
            )
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    def test_403_delete_match_incorrect_persmission(self):
        res = self.client().delete(
            '/matches/2',
            headers=dict(
                Authorization='Bearer ' + self.player_token
            )
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(len(data['message']))


# Make the tests conveniently executable
if __name__ == "__main__":
    # THIS IS ONLY FOR UNIT TESTING!
    db_drop_and_create_all()
    unittest.main()
