from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://portfolio:portfolio123@localhost:5432/portfoliodb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blog')
def blog():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post = Post(title=request.form['title'], content=request.form['content'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('new_post.html')

@app.route('/blog/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
