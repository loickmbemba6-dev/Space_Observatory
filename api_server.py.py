import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = 'D:/extraction_sn/supernovae.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/supernovae', methods=['GET'])
def get_supernovae():
    search = request.args.get('search', '')
    limit = request.args.get('limit', 50)
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT name, claimedtype, redshift, maxappmag, phot_count, ra, dec, host FROM supernovae"
    params = []
    if search:
        query += " WHERE name LIKE ?"
        params.append(f'%{search}%')
    query += " LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/supernovae/<name>', methods=['GET'])
def get_supernova_details(name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM supernovae WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        data = dict(row)
        for k, v in data.items():
            if v is None:
                data[k] = ""
        return jsonify(data)
    return jsonify({"error": "Supernova non trouvée"}), 404

if __name__ == '__main__':
    print("Serveur API demarre sur http://localhost:5000")
    app.run(port=5000, debug=True)
