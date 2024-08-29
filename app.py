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

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        data = request.get_json()
        # Verifica que 'text' y 'post_id' estén presentes en los datos
        if 'text' not in data or 'post_id' not in data:
            return jsonify({'error': 'Missing fields'}), 400
        
        # Verifica que el post_id sea válido
        if not Post.query.get(data['post_id']):
            return jsonify({'error': 'Invalid post_id'}), 400

        comment = Comment(text=data['text'], post_id=data['post_id'])
        db.session.add(comment)
        db.session.commit()
        return jsonify({'id': comment.id, 'text': comment.text, 'post_id': comment.post_id}), 201

    comments = Comment.query.all()
    return jsonify([{'id': comment.id, 'text': comment.text, 'post_id': comment.post_id} for comment in comments])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
