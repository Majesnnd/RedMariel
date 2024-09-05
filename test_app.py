import unittest
from app import app, db, User, Post, Comment

class SimpleTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test para crear un usuario
    def test_create_user(self):
        response = self.app.post('/users', json={'name': 'Test User'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Test User', response.data)

    # Test para obtener usuarios (sin usuarios creados debería devolver una lista vacía)
    def test_get_users_empty(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    # Test para obtener usuarios (después de crear un usuario)
    def test_get_users_after_creation(self):
        self.app.post('/users', json={'name': 'User 1'})
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'User 1')
    
    def test_create_post(self):
        response = self.app.post('/posts', json={'title': 'Test Post', 'content': 'This is a test post content'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Test Post', response.data)
    

    '''
    def test_create_post_without_title(self):
        response = self.app.post('/posts', json={'content': 'Post without title'})
        self.assertEqual(response.status_code, 400)
    '''

    
    def test_create_comment_without_post_id(self):
        response = self.app.post('/comments', json={'text': 'Comment without post_id'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing fields', response.data)


    
    def test_user_exists_in_db(self):
        self.app.post('/users', json={'name': 'Test User'})
        with app.app_context():
            user = User.query.filter_by(name='Test User').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'Test User')

if __name__ == '__main__':
    unittest.main()

