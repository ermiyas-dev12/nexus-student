from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT,
        author TEXT DEFAULT 'Anonymous',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/community')
def community():
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY created_at DESC')
    posts = c.fetchall()
    conn.close()
    return render_template('community.html', posts=posts)

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message', '').lower()

    if 'work' in msg or 'hours' in msg:
        reply = "On a Russian student visa, you can work <strong>only with a valid work permit</strong>. Usually limited to your region and university period. Check with your university for authorization."
    elif 'visa' in msg or 'extend' in msg:
        reply = "To extend your visa you need: <strong>invitation letter from university</strong>, valid passport, migration card, registration. Apply through the <strong>Ministry of Internal Affairs (MVD)</strong> before expiry."
    elif 'doctor' in msg or 'hospital' in msg or 'insurance' in msg:
        reply = "Medical services require <strong>health insurance</strong>. Visit university clinics or local hospitals. Emergency services are available by calling <strong>103</strong>."
    elif 'tenant' in msg or 'landlord' in msg or 'deposit' in msg:
        reply = "Rental agreements are usually private. Always sign a <strong>written contract</strong>. Registration at your address is <strong>mandatory</strong> for visa compliance."
    elif 'work permit' in msg:
        reply = "You need a <strong>work permit</strong> issued by authorities. Many universities help students apply. Working without it is illegal."
    elif 'stay' in msg or 'after study' in msg:
        reply = "After graduation, you must <strong>change your visa type</strong> (work visa or residence permit). Russia does not offer an automatic post-study work visa."
    else:
        reply = "Check official information from the <strong>Ministry of Internal Affairs (MVD)</strong>, your <strong>university international office</strong>, or visit our <strong>Resources</strong> page."

    return jsonify({'reply': reply})

@app.route('/api/post', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('title', '').strip()
    body = data.get('body', '').strip()
    author = data.get('author', 'Anonymous').strip()

    if not title:
        return jsonify({'error': 'Title required'}), 400

    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (title, body, author) VALUES (?, ?, ?)',
              (title, body, author))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)