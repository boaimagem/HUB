from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path
import requests
from datetime import datetime

DB_PATH = Path('app/data.db')

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            copyright_info TEXT NOT NULL
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS plays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_name TEXT NOT NULL,
            title TEXT NOT NULL,
            played_at TEXT NOT NULL
        )
        '''
    )
    conn.commit()
    conn.close()

def store_play(artist_name: str, title: str, played_at: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO plays (artist_name, title, played_at) VALUES (?, ?, ?)',
        (artist_name, title, played_at),
    )
    conn.commit()
    conn.close()

def fetch_shoutcast(url: str):
    """Fetch current song info from a Shoutcast server."""
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        song = data.get('songtitle') or data.get('song')
        if song:
            if ' - ' in song:
                artist, title = song.split(' - ', 1)
            else:
                artist, title = '', song
            store_play(artist.strip(), title.strip(), datetime.utcnow().isoformat())
            return True
    except Exception:
        pass
    return False

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM artists')
    artists = cur.fetchall()
    conn.close()
    return render_template('index.html', artists=artists)

@app.route('/artist/<int:artist_id>')
def artist_detail(artist_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, name, copyright_info FROM artists WHERE id = ?', (artist_id,))
    artist = cur.fetchone()
    conn.close()
    if artist:
        return render_template('artist.html', artist=artist)
    return 'Artist not found', 404

@app.route('/new', methods=['GET', 'POST'])
def new_artist():
    if request.method == 'POST':
        name = request.form['name']
        info = request.form['info']
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('SELECT id FROM artists WHERE lower(name) = lower(?)', (name,))
        if cur.fetchone():
            conn.close()
            return 'Artista duplicado', 400
        cur.execute('INSERT INTO artists (name, copyright_info) VALUES (?, ?)', (name, info))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new_artist.html')

@app.route('/api/shoutcast/plays', methods=['POST'])
def shoutcast_play():
    data = request.get_json(force=True)
    artist = data.get('artist') or ''
    title = data.get('title') or ''
    played_at = data.get('played_at') or datetime.utcnow().isoformat()
    store_play(artist, title, played_at)
    return {'status': 'ok'}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
