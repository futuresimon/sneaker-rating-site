# Note: the set up for the flask app was done with help by the flask tutorial on their website
# all the imports
import os
import sqlite3
#import secrets
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory
from werkzeug.security import generate_password_hash, \
     check_password_hash
from werkzeug.utils import secure_filename

#Path and allowed file types
# from the flask upload file tutorial: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
UPLOAD_FOLDER = '/home/simono/public_html/sneakeragg/sneakeragg/pictures'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#end flask upload tutorial help

#this set up is from the Flask quick start guide
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , sneaker_agg.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sneakeragg.db'),
    SECRET_KEY='RGzzMnLnaGUznOx2b1SSZvmeWuHa2dKY',
    USERNAME='admin',
    PASSWORD='adminPassword',
    SESSION_COOKIE_HTTPONLY = True
))
app.config.from_envvar('SNEAKERAGG_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
#end help from quickstart guide

#Main homepage function
@app.route('/')
def show_sneakers():
    one = 1
    db = get_db()
    cur = db.execute('SELECT id, name, brand, user_id, image_path FROM sneakers WHERE display = ? ORDER BY id DESC',
                 [one])
    sneakers = cur.fetchall()
    return render_template('show_sneakers.html', sneakers=sneakers)

#About and search functions
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        one = 1
        db = get_db()
        cur = db.execute('SELECT id, name, brand, user_id, image_path FROM sneakers WHERE brand = ? AND display = ? order by id desc',
                     [request.form['brand'], one])
        sneakers = cur.fetchall()
        return render_template('show_sneakers.html', sneakers=sneakers)
    return render_template('show_sneakers.html', sneakers=sneakers)

#Add comment and retrieve comment functions
#this will be similar to the show sneakers, but now we'll just show the comments
@app.route('/comments/<sneakerid>')
def comments(sneakerid):
    one = 1
    db = get_db()
    cur = db.execute('SELECT id, review, rating, user_id, sneaker_id FROM reviews WHERE sneaker_id = ? AND display = ? order by id desc',
                 [sneakerid, one])
    comments = cur.fetchall()
    cur2 = db.execute('SELECT AVG(reviews.rating) AS averageRating, sneakers.name FROM reviews, sneakers WHERE reviews.sneaker_id = ? AND reviews.sneaker_id = sneakers.id  AND reviews.display = ?',
                 [sneakerid, one])
    average = cur2.fetchall()
    cur3 = db.execute('SELECT id, website, review, user_id, sneaker_id FROM admin_reviews WHERE sneaker_id =? AND display = ? ORDER BY id DESC',
                 [sneakerid, one])
    websiteComments = cur3.fetchall()
    return render_template('comments.html', websiteComments = websiteComments, comments = comments, averages = average, sneakerid = sneakerid)

@app.route('/add_comment/<sneakerid>', methods=['POST'])
def add_comment(sneakerid):
    if not session.get('logged_in'):
        abort(401)
    one = 1
    db = get_db()
    db.execute('insert into reviews (review, rating, user_id, sneaker_id, display) values (?, ?, ?, ?, ?)',
                 [request.form['comment'], request.form['score'],session['id'], sneakerid, one])
    db.commit()
    flash('New comment was successfully posted')
    return redirect(url_for('comments', sneakerid = sneakerid))

@app.route('/add_comment_admin/<sneakerid>', methods=['POST'])
def add_comment_admin(sneakerid):
    if not session.get('logged_in'):
        abort(401)
    if session['isAdmin'] != 1:
        abort(401)
    one = 1
    db = get_db()
    db.execute('insert into admin_reviews (website, review, user_id, sneaker_id, display) values (?, ?, ?, ?, ?)',
                 [request.form['website'], request.form['website_comment'],session['id'], sneakerid, one])
    db.commit()
    flash('New website comment was successfully posted')
    return redirect(url_for('comments', sneakerid = sneakerid))


#Send message, and profile functions
@app.route('/send_message', methods=['GET','POST'])
def send_message():
    if not session.get('logged_in'):
        abort(401)
    #if not session['id'] == int(senderid):
    #    abort(401)
    if request.method == 'POST':
        one = 1
        db = get_db()
        cur = db.execute('SELECT COUNT(*), id FROM users WHERE username = ?',
                     [request.form['username']])
        recieveridFetch = cur.fetchall()
        for row in recieveridFetch:
            if row[0] > 1:
                error = 'Couldnt send. More than one user found with that name.'
            elif row[0] == 0:
                error = 'Couldnt send. No user found with that name.'
            else:
                recieverid = row[1]
                db.execute('INSERT INTO messages (message_body, sender_id, reciever_id) VALUES (?, ?, ?)',
                             [request.form['message'], session['id'], recieverid])
                db.commit()
                flash('Message sent')
                return redirect(url_for('profile', userid = session['id']))
    return redirect(url_for('profile', error = error, userid = session['id']))

@app.route('/profile/<userid>')
def profile(userid):
    if not session.get('logged_in'):
        abort(401)
    if not session['id'] == int(userid):
        abort(401)
    #one = 1
    db = get_db()
    cur = db.execute('SELECT messages.message_body, messages.reciever_id, users.username FROM messages, users WHERE messages.reciever_id = users.id AND messages.reciever_id = ?',
                 [userid])
    messages = cur.fetchall()
    return render_template('profile.html', messages = messages, userid = userid)


#Upload, and delete sneaker functions.
# from the flask upload file tutorial: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# end help from flask upload file tutorial

@app.route('/add_sneaker', methods=['GET', 'POST'])
def add_sneaker():
    error = None
    if request.method == 'POST':
        #help from file upload tutorial http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #end help from file upload tutorial
            #check if certain conditions are fulfilled
            if not session.get('logged_in'):
                abort(401)
            if session['isAdmin'] != 1:
                abort(401)
            #insert into DB
            one = 1
            db = get_db()
            db.execute('insert into sneakers (name, brand, image_path, display, user_id) values (?, ?, ?, ?, ?)',
                [request.form['title'], request.form['brand'],'/uploads/' + filename, one, session['id']])
            db.commit()
            return redirect(url_for('show_sneakers'))
    return redirect(url_for('show_sneakers'))

@app.route('/delete_sneaker/<userid>/<sneakerid>')
def delete_sneaker(userid, sneakerid):
    #make sure this action is permitted
    if not session.get('logged_in'):
        abort(401)
    if not session['id'] == int(userid):
        abort(401)
    zero = 0
    db = get_db()
    db.execute('UPDATE sneakers SET display = ? WHERE id = ?',
        [zero, sneakerid])
    db.commit()
    flash('Deleted')
    return redirect(url_for('show_sneakers'))

#help from file upload tutorial
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
#end derivation

#Favorite, unfavorite, and retrieve favorites functions
@app.route('/add_to_favorites/<sneakerid>')
def add_to_favorites(sneakerid):
    if not session.get('logged_in'):
        abort(401)
    one = 1
    db = get_db()
    db.execute('insert into favorites (user_id, sneaker_id, display) values (?, ?, ?)',
                 [session['id'], sneakerid, one])
    db.commit()
    flash('Added to favorites')
    return redirect(url_for('show_sneakers'))

@app.route('/unfavorite/<userid>/<sneakerid>')
def unfavorite(userid, sneakerid):
    if not session.get('logged_in'):
        abort(401)
    if not session['id'] == int(userid):
        abort(401)
    zero = 0
    db = get_db()
    db.execute('UPDATE favorites SET display = ? WHERE sneaker_id = ? and user_id = ?',
        [zero, sneakerid, userid])
    db.commit()
    flash('Unfavorited')
    return redirect(url_for('favorites',userid=session['id']))

@app.route('/favorites/<userid>')
def favorites(userid):
    db = get_db()
    if session['id'] == int(userid):
        one = 1
        cur = db.execute('SELECT favorites.sneaker_id, favorites.user_id, sneakers.name, sneakers.image_path FROM FAVORITES, SNEAKERS WHERE (favorites.sneaker_id = sneakers.id) AND favorites.display = ? AND favorites.user_id = ?',
                [one, userid])
        favorites=cur.fetchall()
        return render_template('favorites.html', favorites = favorites)
    else:
        flash('You cant creep on other peoples favorites')
        return redirect(url_for('show_sneakers'))

#Normal sign up, admin sign up, and log in functions

@app.route('/signup', methods=['POST','GET'])
def signup():
    error = None
    if request.method == 'POST':
        if request.form['password'] != request.form['password']:
            error = 'Passwords dont match. Try again.'
        else:
            pw_hash = generate_password_hash(request.form['password'])
            db = get_db()
            zero = 0
            db.execute('insert into users (is_admin, username, password) values (?, ?, ?)',
                         [zero, request.form['username'], pw_hash])
            db.commit()
            flash('You signed up!')
            return redirect(url_for('show_sneakers'))
    return render_template('signup.html', error=error)

@app.route('/admin', methods=['POST','GET'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['password'] != request.form['password']:
            error = 'Passwords dont match. Try again.'
        elif request.form['admin_password'] != app.config['PASSWORD']:
            error = 'Wrong admin password. Try again.'
        else:
            pw_hash = generate_password_hash(request.form['password'])
            db = get_db()
            one = 1
            db.execute('insert into users (is_admin, username, password) values (?, ?, ?)',
                         [one, request.form['username'], pw_hash])
            db.commit()
            flash('You signed up!')
            return redirect(url_for('show_sneakers'))
    return render_template('admin.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('SELECT COUNT(*), id, username, is_admin, password FROM users WHERE username=?',
                 [request.form['username']])
        users = cur.fetchall()
        for row in users:
            if row[0] > 1:
                 error = 'Couldnt log in. More than one user found with that name'
            elif row[0] == 0:
                 error = 'Couldnt log in. No user found with that name.'
            elif check_password_hash(row[4], request.form['password']) == False:
                 error = 'Invalid password'
            else:
                 session['logged_in'] = True
                 session['id'] = row[1]
                 session['username'] = row[2]
                 session['isAdmin'] = row[3]
                 session['token'] = os.urandom(24)
                 flash('You were logged in')
                 return redirect(url_for('show_sneakers'))
    return render_template('login.html', error=error)

#from the set up tutorial
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('isAdmin', None)
    session.pop('token', None)
    flash('You were logged out')
    return redirect(url_for('show_sneakers'))
