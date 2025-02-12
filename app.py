from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Set up rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["250 per day", "65 per hour"]  # Adjust as needed
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'session-token'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

topics = []

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('forum'))
    return render_template('index.html')

@app.route('/set-username', methods=['POST'])
def set_username():
    session['username'] = request.form['username']
    return redirect(url_for('forum'))

@app.route('/forum')
def forum():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('forum.html', topics=topics, username=session['username'])

@app.route('/new-topic', methods=['POST'])
def new_topic():
    title = request.form['title']
    username = session['username']
    new_topic = {
        'title': title,
        'username': username,
        'messages': []
    }
    topics.append(new_topic)
    return redirect(url_for('forum'))

@app.route('/new-message', methods=['POST'])
def new_message():
    topic_index = int(request.form['topic_index'])
    username = session['username']
    message = request.form['message']
    new_message = {
        'username': username,
        'message': message
    }
    topics[topic_index]['messages'].append(new_message)
    return redirect(url_for('forum'))

if __name__ == '__main__':
    app.run(debug=True)
