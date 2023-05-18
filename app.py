"""Blogly application."""

from flask import Flask, request, render_template, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'something-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

DEFAULT_IMAGE_URL = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'

@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def list_users():

    users = User.query.all()
    
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_add_user():
    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id)
    
    return render_template('details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):

    user = User.query.get(user_id)

    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    
    user = User.query.get(user_id)

    user.first_name = request.form['first_name'] or user.first_name
    user.last_name = request.form['last_name'] or user.last_name
    user.image_url = request.form['image_url'] or DEFAULT_IMAGE_URL

    db.session.add(user)
    db.session.commit()

    return redirect(f'/user/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('new_post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_new_post(user_id):
    
    new_post = Post(title=request.form['title'], 
                    content=request.form['content'], 
                    user_id=user_id)
    
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_posts(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('show_posts.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_post(post_id):

    post = Post.query.get(post_id)

    tags = Tag.query.all()

    for tag in tags:
        try: 
            if request.form[tag.name]:
                post.tags.append(tag)
        except:
            print('Not selected')
            

    print('***************************')
    print(request.form)

    post.title = request.form['title'] or post.title
    post.content = request.form['content'] or post.content
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):

    post = Post.query.get(post_id)

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


# ----------------Tags-------------------

@app.route('/tags')
def show_tags():

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tags_show.html', tag=tag) 

@app.route('/tags/new')
def new_tag():
    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    tag = Tag(name=request.form['tag_name'])

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def add_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect('/tags')



