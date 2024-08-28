import unittest
from app import app, db, User, Post, Comment

class FlaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        # Add sample data
        cls.user1 = User(name='John Doe')
        cls.user2 = User(name='Jane Smith')
        db.session.add(cls.user1)
        db.session.add(cls.user2)

        cls.post1 = Post(title='First Post', content='Content of the first post')
        cls.post2 = Post(title='Second Post', content='Content of the second post')
        db.session.add(cls.post1)
        db.session.add(cls.post2)

        cls.comment1 = Comment(text='First comment on first post', post_id=cls.post1.id)
        cls.comment2 = Comment(text='First comment on second post', post_id=cls.post2.id)
        db.session.add(cls.comment1)
        db.session.add(cls.comment2)
        
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        cls.app_context.pop()

    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'John Doe')
        self.assertEqual(data[1]['name'], 'Jane Smith')

    def test_post_user(self):
        response = self.client.post('/users', json={'name': 'Alice Johnson'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Alice Johnson')

    def test_get_posts(self):
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'First Post')
        self.assertEqual(data[1]['title'], 'Second Post')

    def test_post_post(self):
        response = self.client.post('/posts', json={'title': 'Third Post', 'content': 'Content of the third post'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Third Post')

    def test_get_comments(self):
        response = self.client.get('/comments')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['text'], 'First comment on first post')
        self.assertEqual(data[1]['text'], 'First comment on second post')

    def test_post_comment(self):
        response = self.client.post('/comments', json={'text': 'New comment', 'post_id': self.post1.id})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'New comment')
        self.assertEqual(data['post_id'], self.post1.id)

if __name__ == '__main__':
    unittest.main()
