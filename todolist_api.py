from flask import Flask, jsonify, request, g
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

app.config['DATABASE'] = 'todolist.db'

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/api/items", methods=["GET"])
def get_items():
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2]) for row in entries]
    return jsonify(tdlist)


@app.route("/api/add", methods=["POST"])
def add_entry():
    db = get_db()
    new_todo = request.get_json()
    db.execute('insert into entries (what_to_do, due_date) values (?, ?)',
               (new_todo["what_to_do"], new_todo["due_date"]))
    db.commit()
    return jsonify({"message": "Added Successfully!"})


@app.route("/api/delete/<item>", methods=["POST"])
def delete_entry(item):
    db = get_db()
    db.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
    db.commit()
    return jsonify({"message": "Deleted Successfully!"})


@app.route("/api/mark/<item>", methods=["POST"])
def mark_as_done(item):
    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE what_to_do='"+item+"'")
    db.commit()
    return jsonify({"message": "Marked as Done!"})


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
