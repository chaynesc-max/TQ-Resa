
# Office Booking App (Flask) - Demo

This is a minimal Flask application that demonstrates:
- Displaying floor plan images per site (Montréal / Québec)
- Clickable areas on the floor plan to inspect rooms
- Simple booking API with overlap check (SQLite)

## Run locally
1. Ensure Python 3.10+ installed.
2. Install dependencies:
   ```
   pip install Flask pillow
   ```
3. Run:
   ```
   python app.py
   ```
4. Open http://127.0.0.1:5000/

## Files
- app.py : Flask application
- data.db : sample SQLite DB (rooms + bookings)
- templates/ : HTML templates
- static/images/ : generated placeholder floor plan PNGs

This is a starting point; you can:
- Replace images with your real floor plans
- Update `coords` in the `rooms` table to match real positions
- Add authentication, integration with Microsoft Graph, and a nicer UI.
