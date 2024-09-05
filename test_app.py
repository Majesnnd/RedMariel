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
    
    # Test para crear un post
    def test_create_post(self):
        response = self.app.post('/posts', json={'title': 'Test Post', 'content': 'This is a test post content'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Test Post', response.data)

    # Test para eliminar un usuario existente
    def test_delete_user(self):
        # Crear un usuario primero
        self.app.post('/users', json={'name': 'User to delete'})
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted successfully', response.data)

    # Test para intentar eliminar un usuario no existente
    def test_delete_user_not_found(self):
        response = self.app.delete('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    # Test para eliminar un post existente
    def test_delete_post(self):
        # Crear un post primero
        self.app.post('/posts', json={'title': 'Post to delete', 'content': 'Content to delete'})
        response = self.app.delete('/posts/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post deleted successfully', response.data)

    # Test para intentar eliminar un post no existente
    def test_delete_post_not_found(self):
        response = self.app.delete('/posts/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Post not found', response.data)

    # Test para crear un comentario
    def test_create_comment(self):
        # Crear un post primero para asociar el comentario
        self.app.post('/posts', json={'title': 'Post for comment', 'content': 'Post content'})
        response = self.app.post('/comments', json={'text': 'Test comment', 'post_id': 1})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Test comment', response.data)

    # Test para intentar crear un comentario con campos faltantes
    def test_create_comment_missing_fields(self):
        response = self.app.post('/comments', json={'text': 'Missing post_id'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing fields', response.data)

    # Test para intentar crear un comentario con un post_id inválido
    def test_create_comment_invalid_post_id(self):
        response = self.app.post('/comments', json={'text': 'Invalid post_id', 'post_id': 999})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid post_id', response.data)

    # Test para eliminar un comentario existente
    def test_delete_comment(self):
        # Crear un post y un comentario primero
        self.app.post('/posts', json={'title': 'Post for comment', 'content': 'Post content'})
        self.app.post('/comments', json={'text': 'Comment to delete', 'post_id': 1})
        response = self.app.delete('/comments/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comment deleted successfully', response.data)

    # Test para intentar eliminar un comentario no existente
    def test_delete_comment_not_found(self):
        response = self.app.delete('/comments/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Comment not found', response.data)
