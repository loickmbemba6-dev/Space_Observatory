
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "supernovae.db"


def get_db():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Base de données introuvable : {DB_PATH}"
        )

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "database_exists": DB_PATH.exists()
    })


@app.route("/api/supernovae", methods=["GET"])
def get_supernovae():
    search = request.args.get("search", "").strip()

    try:
        limit = int(request.args.get("limit", 50))
        limit = max(1, min(limit, 500))
    except ValueError:
        return jsonify({"error": "Invalid limit"}), 400

    try:
        with get_db() as conn:
            query = """
                SELECT name, claimedtype, redshift,
                       maxappmag, phot_count, ra, dec, host
                FROM supernovae
            """
            params = []

            if search:
                query += " WHERE name LIKE ?"
                params.append(f"%{search}%")

            query += " LIMIT ?"
            params.append(limit)

            results = [
                dict(row)
                for row in conn.execute(query, params).fetchall()
            ]

        return jsonify(results)

    except (sqlite3.Error, FileNotFoundError) as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/supernovae/<name>", methods=["GET"])
def get_supernova_details(name):
    try:
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM supernovae WHERE name = ?",
                (name,)
            ).fetchone()

        if row:
            return jsonify(dict(row))

        return jsonify({"error": "Supernova non trouvée"}), 404

    except (sqlite3.Error, FileNotFoundError) as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
