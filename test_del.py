from app import app
import unittest

class FlaskappTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
		
    def test_deluser_status_code(self):
        result = self.app.delete('/api/v3/users',
                               data='{"username":"tmp_usr"}',
                               content_type = 'application/json')
        self.assertEqual(result.status_code, 200)