from flask import Flask, render_template, request, url_for, jsonify
import json
import string, random
import time
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# =========================
# CONFIG
# =========================
FIVE_DAYS = 5 * 24 * 60 * 60  # 5 days (production)

# =========================
# UTILS
# =========================
def clean_old_data(data):
    current = time.time()
    return {
        k: v for k, v in data.items()
        if current - v.get("created_at", current) < FIVE_DAYS
    }

def generate_unique_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {}

    # 🔥 CLEAN HERE
    data = clean_old_data(data)

    # save cleaned data
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    your_name = request.form.get("your_name")
    crush_name = request.form.get("crush_name")
    your_paragraph = request.form.get("your_paragraph")

    unique_id = generate_unique_id()

    data = load_data()

    data[unique_id] = {
        "your_name": your_name,
        "crush_name": crush_name,
        "your_paragraph": your_paragraph,
        "response": None,
        "created_at": time.time()
    }

    save_data(data)

    love_link = url_for("love_page", unique_id=unique_id, _external=True)
    status_link = url_for("check_response", unique_id=unique_id, _external=True)

    return jsonify({
        "love_link": love_link,
        "status_link": status_link
    })

@app.route("/love/<unique_id>")
def love_page(unique_id):
    data = load_data()

    if unique_id not in data:
        return "Invalid link!"

    entry = data[unique_id]

    return render_template(
        "love.html",
        message=entry["your_paragraph"],
        your_name=entry["your_name"],
        unique_id=unique_id
    )

@app.route("/response/<unique_id>/<answer>")
def save_response(unique_id, answer):
    data = load_data()

    if unique_id not in data:
        return jsonify({"status": "error", "message": "Invalid link"})

    data[unique_id]["response"] = answer
    save_data(data)

    return jsonify({"status": "success"})

@app.route("/status/<unique_id>")
def check_response(unique_id):
    data = load_data()

    if unique_id not in data:
        return render_template(
            "status.html",
            status="invalid",
            message="Invalid link ❌"
        )

    response = data[unique_id].get("response")

    if response:
        return render_template(
            "status.html",
            status="answered",
            message=f"They selected {response.upper()} 💖"
        )
    else:
        return render_template(
            "status.html",
            status="waiting",
            message="Your crush has not responded yet ⏳"
        )

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)