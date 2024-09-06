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

    
    def test_create_user(self):
        response = self.app.post('/users', json={'name': 'Test User'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Test User', response.data)

    
    def test_get_users_empty(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

     
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

    
    def test_delete_user(self):
        
        self.app.post('/users', json={'name': 'User to delete'})
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted successfully', response.data)

    
    def test_delete_user_not_found(self):
        response = self.app.delete('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    
    def test_delete_post(self):
        self.app.post('/posts', json={'title': 'Post to delete', 'content': 'Content to delete'})
        response = self.app.delete('/posts/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post deleted successfully', response.data)

    #
    def test_delete_post_not_found(self):
        response = self.app.delete('/posts/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Post not found', response.data)

    '''
    def test_create_comment(self):
        self.app.post('/posts', json={'title': 'Post for comment', 'content': 'Post content'})
        response = self.app.post('/comments', json={'text': 'Test comment', 'post_id': 1})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Test comment', response.data)

    
    def test_create_comment_missing_fields(self):
        response = self.app.post('/comments', json={'text': 'Missing post_id'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing fields', response.data)

    
    def test_create_comment_invalid_post_id(self):
        response = self.app.post('/comments', json={'text': 'Invalid post_id', 'post_id': 999})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid post_id', response.data)

    
    def test_delete_comment(self):
        self.app.post('/posts', json={'title': 'Post for comment', 'content': 'Post content'})
        self.app.post('/comments', json={'text': 'Comment to delete', 'post_id': 1})
        response = self.app.delete('/comments/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comment deleted successfully', response.data)

    
    def test_delete_comment_not_found(self):
        response = self.app.delete('/comments/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Comment not found', response.data)
    '''
