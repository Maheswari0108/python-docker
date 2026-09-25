from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "movie-secret-key"

# In-memory store for bookings
bookings = []

# Available movies
MOVIES = [
    {"id": 1, "title": "Inception", "price": 250, "showtime": "10:00 AM"},
    {"id": 2, "title": "Interstellar", "price": 300, "showtime": "01:30 PM"},
    {"id": 3, "title": "The Dark Knight", "price": 280, "showtime": "04:45 PM"},
    {"id": 4, "title": "Dune: Part Two", "price": 350, "showtime": "08:00 PM"},
]


@app.route("/")
def index():
    return render_template("index.html", movies=MOVIES, bookings=bookings)


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name", "").strip()
    movie_id = request.form.get("movie_id")
    seats = request.form.get("seats", "1")

    if not name or not movie_id or not seats:
        flash("Please fill in all fields.", "error")
        return redirect(url_for("index"))

    movie = next((m for m in MOVIES if str(m["id"]) == str(movie_id)), None)
    if not movie:
        flash("Invalid movie selected.", "error")
        return redirect(url_for("index"))

    try:
        seats = int(seats)
        if seats < 1 or seats > 10:
            raise ValueError
    except ValueError:
        flash("Number of seats must be between 1 and 10.", "error")
        return redirect(url_for("index"))

    total = seats * movie["price"]
    booking = {
        "id": len(bookings) + 1,
        "name": name,
        "movie": movie["title"],
        "showtime": movie["showtime"],
        "seats": seats,
        "total": total,
    }
    bookings.append(booking)
    flash(f"Booking confirmed for {name}! Total: ₹{total}", "success")
    return redirect(url_for("index"))


@app.route("/cancel/<int:booking_id>", methods=["POST"])
def cancel(booking_id):
    global bookings
    bookings = [b for b in bookings if b["id"] != booking_id]
    flash("Booking cancelled.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
