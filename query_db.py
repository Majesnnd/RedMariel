from app import app, db
from models import User, Post, Comment

with app.app_context():
    # Consultar datos de User
    users = User.query.all()
    print("Usuarios:")
    for user in users:
        print(f'ID: {user.id}, Name: {user.name}')

    # Consultar datos de Post
    posts = Post.query.all()
    print("\nPublicaciones:")
    for post in posts:
        print(f'ID: {post.id}, Title: {post.title}, Content: {post.content}')

    # Consultar datos de Comment
    comments = Comment.query.all()
    print("\nComentarios:")
    for comment in comments:
        print(f'ID: {comment.id}, Text: {comment.text}, Post ID: {comment.post_id}')
