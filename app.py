from flask import Flask, request, jsonify, render_template
from models import db, User, Post, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        user = User(name=data['name'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'name': user.name}), 201
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        data = request.get_json()
        post = Post(title=data['title'], content=data['content'])
        db.session.add(post)
        db.session.commit()
        return jsonify({'id': post.id, 'title': post.title, 'content': post.content}), 201
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content} for post in posts])

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        data = request.get_json()
        if 'text' not in data or 'post_id' not in data:
            return jsonify({'error': 'Missing fields'}), 400
        
        if not Post.query.get(data['post_id']):
            return jsonify({'error': 'Invalid post_id'}), 400

        comment = Comment(text=data['text'], post_id=data['post_id'])
        db.session.add(comment)
        db.session.commit()
        return jsonify({'id': comment.id, 'text': comment.text, 'post_id': comment.post_id}), 201

    comments = Comment.query.all()
    return jsonify([{'id': comment.id, 'text': comment.text, 'post_id': comment.post_id} for comment in comments])

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
