import os
import json
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from utils.get_password import get_password

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template("posts.html", posts=posts)


@app.route('/posts/<int:id>')
def post_detail(id):
    post = Post.query.get(id)
    return render_template("post.html", post=post)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    post = Post.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error deleting the post"


@app.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        post = Post(title=title, intro=intro, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'error while adding post'
    else:
        return render_template("create_post.html")


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    post = Post.query.get(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.intro = request.form['intro']
        post.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'error while updating post'
    else:
        return render_template("update_post.html", post=post)
    

@app.route('/pass-gen', methods=['POST', 'GET'])
def pass_gen():
    if request.method == "POST":
        json.dumps(request.form)
        length = int(request.form['length'])
        special = False if request.form.get('special') is None else True
        numbers = False if request.form.get('numbers') is None else True
        uppercase = False if request.form.get('uppercase') is None else True
        
        password = get_password(length, special, numbers, uppercase)
    
        return render_template("pass_gen.html", password=password, length=length, special=special, numbers=numbers, uppercase=uppercase)
    else:
        password = get_password(12, False, False, False)
        return render_template("pass_gen.html", password=password, length=12, special=False, numbers=False, uppercase=False)


if __name__ == "__main__":
    app.run(debug=True)