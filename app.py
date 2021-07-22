"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'scale-the-summit'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_users():
    return redirect('/users')

##### User routes #####

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('users/user-list.html', users = users)

@app.route('/users/new')
def show_new_user_form():
    """Get the form to create a new user"""
    return render_template('users/create-user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Add new user to the database"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show info about a user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/user.html', user = user)

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """Show the edit page for a user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit-user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edit user"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

##### Post routes #####

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Show the Add New Post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new-post.html', user = user, tags = tags)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def add_new_post(id):
    """Add new post"""
    user = User.query.get_or_404(id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=id, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f'Post {new_post.title} successfully added')

    return redirect(f'/users/{id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', post = post)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """Go to edit page for post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('posts/edit-post.html', post = post, tags = tags)

@app.route("/posts/<int:post_id>/edit", methods=['POST'])
def edit_post(post_id):
    """Edit post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f'Post {post.title} successfully edited')
    
    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f'Post {post.title} successfully deleted')
    
    return redirect(f'/users/{post.user_id}')

##### Tags #####

@app.route('/tags')
def show_tags():
    """Show all tags in database"""
    tags = Tag.query.all()
    return render_template('tags/tags.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """Show a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show-tag.html', tag = tag)

@app.route('/tags/new')
def show_add_new_tag():
    """Got to add tag form"""
    return render_template('tags/create-tag.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    """Create a new tag and redirect to tag list"""
    name = request.form['name']

    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Show form for editing tag"""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tags/edit-tag.html', tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name']

    tag.name = name

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete tag"""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')