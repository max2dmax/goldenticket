from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"  # for session

KEY = "imrich"  # your VIP access key

def load_tickets():
    with open("tickets.json", "r") as f:
        data = json.load(f)
    return data["tickets"]

def save_tickets(tickets):
    with open("tickets.json", "w") as f:
        json.dump({"tickets": tickets}, f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("key") == KEY:
            session["has_key"] = True
        else:
            session["has_key"] = False

    tickets = load_tickets()
    return render_template("index.html", tickets=tickets, has_key=session.get("has_key", False))

@app.route("/use/<int:ticket_id>")
def use_ticket(ticket_id):
    if not session.get("has_key"):
        return redirect(url_for("index"))
    tickets = load_tickets()
    if tickets[ticket_id]:
        tickets[ticket_id] = False
        save_tickets(tickets)
    return redirect(url_for("index"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)