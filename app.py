
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import SignupForm, LoginForm, CVForm, PostForm
from werkzeug.utils import secure_filename
from models import db, User, CV, Post, Comment
from flask_migrate import Migrate
from flask import jsonify
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cv_builder.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


login_manager = LoginManager(app)
login_manager.login_view = 'login'
db.init_app(app)  # This links the db to your app
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    form = PostForm()
    searched_user_id = request.args.get('searched_user_id', type=int)
    posts = None
    post_id = request.args.get('post_id', type=int)  # Get the post ID if provided
    searched_user = None
    searched_user_cv = None
    cv = CV.query.filter_by(user_id=current_user.id).first()
    show_create_post = request.args.get('show_create_post', False)
    posts = Post.query.filter_by(user_id=current_user.id).all()
    
        

    if searched_user_id:
        searched_user = User.query.get_or_404(searched_user_id)
        posts = Post.query.filter_by(user_id=searched_user.id).all()
        comments = Comment.query.filter_by(post_id=post.id).all()
        searched_user_cv = CV.query.filter_by(user_id=searched_user.id).first()
    else:
        posts = Post.query.filter_by(user_id=current_user.id).all()

    current_user_cv = CV.query.filter_by(user_id=current_user.id).first()
    post = None
    comments = []
    if post_id:
        post = Post.query.get_or_404(post_id)
        comments = Comment.query.filter_by(post_id=post.id).all()
    return render_template('dashboard.html', 
                           searched_user=searched_user,
                           cv=cv, 
                           posts=posts,
                           show_create_post=show_create_post, 
                           searched_user_cv=searched_user_cv,
                           current_user_cv=current_user_cv,
                           form=form,
                           comments = comments)
    

@app.route('/cv_form', methods=['GET', 'POST'])
@login_required
def cv_form():
    cv = CV.query.filter_by(user_id=current_user.id).first()
    
    if cv:
        form = CVForm(obj=cv)
    else:
        form = CVForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if cv:
                cv.full_name = form.full_name.data
                cv.email = form.email.data
                cv.phone_number = form.phone_number.data
                cv.date_of_birth = form.date_of_birth.data
                cv.job_title = form.job_title.data
                cv.description = form.description.data
                cv.education = [entry['entry'] for entry in form.education.data]
                cv.experience = [entry['entry'] for entry in form.experience.data]
                cv.projects = [entry['entry'] for entry in form.projects.data]
                cv.skills = [entry['entry'] for entry in form.skills.data]
                cv.certifications = [entry['entry'] for entry in form.certifications.data]
                cv.interests = [entry['entry'] for entry in form.interests.data]
                cv.references = [entry['entry'] for entry in form.references.data]
            else:
                new_cv = CV(
                    user_id=current_user.id,
                    full_name=form.full_name.data,
                    email=form.email.data,
                    phone_number=form.phone_number.data,
                    date_of_birth=form.date_of_birth.data,
                    job_title=form.job_title.data,
                    description=form.description.data,
                    education=[entry['entry'] for entry in form.education.data],
                    experience=[entry['entry'] for entry in form.experience.data],
                    projects=[entry['entry'] for entry in form.projects.data],
                    skills=[entry['entry'] for entry in form.skills.data],
                    certifications=[entry['entry'] for entry in form.certifications.data],
                    interests=[entry['entry'] for entry in form.interests.data],
                    references=[entry['entry'] for entry in form.references.data],
                )
                print("Full Name:", form.full_name.data)
                print("Email:", form.email.data)
                print("Phone Number:", form.phone_number.data)
                print("Date of Birth:", form.date_of_birth.data)
                print("Job Title:", form.job_title.data)
                print("Description:", form.description.data)
                print("Education:", [entry['entry'] for entry in form.education.data])
                print("Experience:", [entry['entry'] for entry in form.experience.data])
                print("Projects:", [entry['entry'] for entry in form.projects.data])
                print("Skills:", [entry['entry'] for entry in form.skills.data])
                print("Certifications:", [entry['entry'] for entry in form.certifications.data])
                print("Interests:", [entry['entry'] for entry in form.interests.data])
                print("References:", [entry['entry'] for entry in form.references.data])
                db.session.add(new_cv)
            db.session.commit()
            return redirect(url_for('view_cv'))
    else:
        print(form.errors)
    return render_template('cv_form.html', form=form)

@app.route('/cv', methods=['GET'])
@login_required
def view_cv():
    searched_user_id = request.args.get('searched_user_id', type=int)
    
    if searched_user_id:
        searched_user = User.query.get_or_404(searched_user_id)
        searched_user_cv = CV.query.filter_by(user_id=searched_user.id).first()
        if searched_user_cv:
            return render_template('cv.html', cv=searched_user_cv)
        else:
            flash(f"No CV found for {searched_user.username}.", "warning")
            return redirect(url_for('dashboard'))
    
    # Fallback to the current user's CV if no searched_user_id is provided
    cv = CV.query.filter_by(user_id=current_user.id).first()
    if cv:
        return render_template('cv.html', cv=cv)
    else:
        flash("No CV found for the current user.", "warning")
        return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/post', methods=['GET', 'POST'])
@login_required

def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        media = form.media.data
        
        # Debugging: Print the current user's ID to ensure it's correctly retrieved
        print(f"User ID: {current_user.id}")
        # Handle file upload
        if media:
            try:
                filename = secure_filename(media.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(f"Saving file to: {file_path}")  # Debugging: Print the file path
                media.save(file_path)
                new_post = Post(title=title, content=content, media=filename, user_id=current_user.id)
            except Exception as e:
                print(f"Error saving file: {e}")
                flash('Error uploading file. Please try again.', 'danger')
                return render_template('dashboard.html', form=form, show_create_post=True, 
                                       posts=Post.query.filter_by(user_id=current_user.id).all(), 
                                       cv=CV.query.filter_by(user_id=current_user.id).first())
        else:
            new_post = Post(title=title, content=content, user_id=current_user.id)
        
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('dashboard'))
    # If validation fails, render the form with error messages
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('dashboard.html', form=form, show_create_post=True, 
                           posts=Post.query.filter_by(user_id=current_user.id).all(), 
                           cv=CV.query.filter_by(user_id=current_user.id).first())

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure that only the owner can delete the post
    if post.user_id != current_user.id:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('dashboard'))

    # If the post has media, remove the file from the filesystem
    if post.media:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.media))
        except Exception as e:
            print(f"Error deleting file: {e}")

    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    content = request.form.get('content')
    if content:
        new_comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    else:
        flash('Comment cannot be empty.', 'danger')
    return redirect(url_for('dashboard', post_id=post_id))  # Redirect back to the dashboard with the post ID

@app.route('/post/<int:post_id>', methods=['GET'])
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('view_post.html', post=post, comments=comments)

@app.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('user_profile.html', user=user, posts=posts)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    query = request.form.get('query')
    results = User.query.filter(User.username.contains(query)).all()
    return render_template('search_results.html', results=results)

@app.route('/search_suggestions')
@login_required
def search_suggestions():
    query = request.args.get('query')
    
    # Filter users whose usernames contain the query string, case-insensitive
    users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    
    # Convert users to a list of dictionaries with id and username
    results = [{'id': user.id, 'username': user.username} for user in users]
    
    return jsonify(results)


@app.route('/user/<int:searched_user_id>/dashboard_partial')
@login_required
def searched_user_dashboard_partial(searched_user_id):
    current_user_id = request.args.get('current_user_id', type=int)
    
    searched_user = User.query.get_or_404(searched_user_id)
    posts = Post.query.filter_by(user_id=searched_user_id).all()
    searched_user_cv = CV.query.filter_by(user_id=searched_user_id).first()
    
    current_user_cv = CV.query.filter_by(user_id=current_user_id).first()

    return render_template('dashboard_partial.html', 
                           searched_user=searched_user, 
                           posts=posts, 
                           searched_user_cv=searched_user_cv, 
                           current_user_cv=current_user_cv)


@app.route('/user/<int:user_id>/cv')
@login_required
def view_searched_user_cv(user_id):
    user = User.query.get_or_404(user_id)
    cv = CV.query.filter_by(user_id=user.id).first()
    return render_template('cv.html', cv=cv)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database tables
    app.run(debug=True)