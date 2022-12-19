from app import app
import unittest

class FlaskappTests(unittest.TestCase):
    c = 0
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.c = 0
        
    def test_api_status_code(self):
        
        result = self.app.get('/api/v3/info')
        self.assertEqual(result.status_code, 200)
    
    def test_add_users_status_code(self):
        
        result = self.app.post('/api/v3/users',
                               data='{"username":"tmp_usr","password":"1234","email":"blabla"}',
                               content_type = 'application/json')
        self.assertEquals(result.status_code, 201)
        
    def test_deluser_status_code(self):
        
        result = self.app.delete('/api/v3/users',
                               data='{"username":"tmp_usr"}',
                               content_type = 'application/json')
        self.assertEqual(result.status_code, 200)
            
      
    def test_add_users_status_code_after_del(self):
       
        result = self.app.post('/api/v3/users',
                               data='{"username":"tmp_usr","password":"1234","email":"blabla"}',
                               content_type = 'application/json')
        self.assertEquals(result.status_code, 201)
