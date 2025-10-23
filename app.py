
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3, os
from datetime import datetime

DB = os.path.join(os.path.dirname(__file__), "data.db")
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/floor/<site>")
def floor(site):
    # show floor plan with clickable areas
    conn = get_db()
    cur = conn.execute("SELECT * FROM rooms WHERE site = ?", (site,))
    rooms = cur.fetchall()
    conn.close()
    return render_template("floor.html", site=site, rooms=rooms)

@app.route("/api/rooms")
def api_rooms():
    site = request.args.get("site")
    conn = get_db()
    if site:
        cur = conn.execute("SELECT * FROM rooms WHERE site = ?", (site,))
    else:
        cur = conn.execute("SELECT * FROM rooms")
    rooms = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rooms)

@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.json
    room_id = data.get("room_id")
    user = data.get("user") or "unknown"
    start = data.get("start")
    end = data.get("end")
    if not (room_id and start and end):
        return jsonify({"status":"error","message":"missing parameters"}), 400
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except Exception as e:
        return jsonify({"status":"error","message":"invalid datetime format (use ISO)"}), 400
    conn = get_db()
    # check overlapping bookings
    cur = conn.execute("""SELECT * FROM bookings WHERE room_id = ? AND NOT (end <= ? OR start >= ?)""",
                       (room_id, start_dt, end_dt))
    conflict = cur.fetchone()
    if conflict:
        conn.close()
        return jsonify({"status":"conflict","message":"Time slot already booked"}), 409
    conn.execute("INSERT INTO bookings(room_id, user, start, end) VALUES (?,?,?,?)",
                 (room_id, user, start_dt, end_dt))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok","message":"booking created"})

@app.route("/api/bookings")
def api_bookings():
    room_id = request.args.get("room_id")
    conn = get_db()
    if room_id:
        cur = conn.execute("SELECT * FROM bookings WHERE room_id = ? ORDER BY start", (room_id,))
    else:
        cur = conn.execute("SELECT * FROM bookings ORDER BY start")
    bookings = [dict(b) for b in cur.fetchall()]
    conn.close()
    # convert datetimes to isoformat strings
    for b in bookings:
        b["start"] = b["start"]
        b["end"] = b["end"]
    return jsonify(bookings)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
