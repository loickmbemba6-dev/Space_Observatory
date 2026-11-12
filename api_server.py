
import sqlite3
from pathlib import Path
from contextlib import closing

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "supernovae.db"

app.config["JSON_SORT_KEYS"] = False


# --------------------------------------------------
# CONNEXION À LA BASE DE DONNÉES
# --------------------------------------------------

def get_db():
    if not DB_PATH.is_file():
        raise FileNotFoundError(
            f"Base de données introuvable : {DB_PATH}"
        )

    conn = sqlite3.connect(
        str(DB_PATH),
        timeout=30
    )

    conn.row_factory = sqlite3.Row
    return conn


# --------------------------------------------------
# CONVERSION DES DONNÉES SQLITE EN JSON
# --------------------------------------------------

def serialize_row(row):
    if row is None:
        return None

    result = {}

    for key in row.keys():
        value = row[key]

        if value is None:
            result[key] = None
        elif isinstance(value, bytes):
            result[key] = value.decode("utf-8", errors="replace")
        else:
            result[key] = value

    return result


# --------------------------------------------------
# ROUTE DE VÉRIFICATION
# --------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "ok",
        "database_exists": DB_PATH.is_file(),
        "database_name": DB_PATH.name
    }), 200


# --------------------------------------------------
# LISTE DES SUPERNOVAE
# --------------------------------------------------

@app.route("/api/supernovae", methods=["GET"])
def get_supernovae():

    search = request.args.get("search", "").strip()

    try:
        limit = int(request.args.get("limit", 50))

        if limit < 1 or limit > 500:
            return jsonify({
                "error": "La limite doit être comprise entre 1 et 500."
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "error": "Paramètre limit invalide."
        }), 400

    try:
        with closing(get_db()) as conn:

            query = """
                SELECT
                    name,
                    claimedtype,
                    redshift,
                    maxappmag,
                    phot_count,
                    ra,
                    dec,
                    host
                FROM supernovae
            """

            params = []

            if search:
                query += " WHERE name LIKE ?"
                params.append(f"%{search}%")

            query += " ORDER BY name LIMIT ?"
            params.append(limit)

            rows = conn.execute(
                query,
                params
            ).fetchall()

            results = [
                serialize_row(row)
                for row in rows
            ]

        return jsonify(results), 200

    except FileNotFoundError as error:
        app.logger.error(str(error))
        return jsonify({"error": str(error)}), 500

    except sqlite3.Error:
        app.logger.exception("Erreur SQLite lors de la recherche.")
        return jsonify({
            "error": "Erreur lors de la lecture de la base de données."
        }), 500


# --------------------------------------------------
# DÉTAILS D'UNE SUPERNOVA
# --------------------------------------------------

@app.route("/api/supernovae/<name>", methods=["GET"])
def get_supernova_details(name):

    try:
        with closing(get_db()) as conn:

            row = conn.execute(
                """
                SELECT *
                FROM supernovae
                WHERE name = ?
                LIMIT 1
                """,
                (name,)
            ).fetchone()

        if row is None:
            return jsonify({
                "error": "Supernova non trouvée."
            }), 404

        return jsonify(serialize_row(row)), 200

    except FileNotFoundError as error:
        app.logger.error(str(error))
        return jsonify({"error": str(error)}), 500

    except sqlite3.Error:
        app.logger.exception("Erreur SQLite lors du chargement.")
        return jsonify({
            "error": "Impossible de charger les détails."
        }), 500


# --------------------------------------------------
# LANCEMENT DU SERVEUR
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
