from flask import Flask, render_template, request, url_for, jsonify
import json
import string, random
import time
import os

app = Flask(__name__)

DATA_FILE = "data.json"

FIVE_DAYS = 5 * 24 * 60 * 60  # 5 days
def clean_old_data(data):
    current = time.time()
    return {
        k: v for k, v in data.items()
        if current - v.get("created_at", current) < FIVE_DAYS
    }

# Ensure data.json exists and is valid
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)
else:
    try:
        with open(DATA_FILE, "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

def generate_unique_id(length=6):
    # """Generate random unique ID"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    your_name = request.form.get("your_name")
    crush_name = request.form.get("crush_name")
    your_paragraph = request.form.get("your_paragraph")

    unique_id = generate_unique_id()

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data = clean_old_data(data)

    data[unique_id] = {
        "your_name": your_name,
        "crush_name": crush_name,
        "your_paragraph": your_paragraph,
        "response": None,
        "created_at": time.time()  
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    # link = url_for("love_page", unique_id=unique_id, _external=True)
    love_link = url_for("love_page", unique_id=unique_id, _external=True)
    status_link = url_for("check_response", unique_id=unique_id, _external=True)

    # return jsonify({"link": link})
    return jsonify({
        "love_link": love_link,
        "status_link": status_link
    })


@app.route("/love/<unique_id>")
def love_page(unique_id):
    # Load existing data safely
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}

    data = clean_old_data(data)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    if unique_id not in data:
        return "Invalid link!"

    entry = data[unique_id]
    your_name = entry["your_name"]
    crush_name = entry["crush_name"]
    your_paragraph = entry["your_paragraph"]

    return render_template("love.html", message=your_paragraph, your_name=your_name, unique_id=unique_id)


# Route to store Yes/No response from crush
@app.route("/response/<unique_id>/<answer>")
def save_response(unique_id, answer):
    # Load existing data
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}

    if unique_id in data:
        data[unique_id]["response"] = answer  # store Yes or No
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Invalid link"})


# Route to check response (sender can use)
@app.route("/status/<unique_id>")
def check_response(unique_id):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}

    data = clean_old_data(data)
        
        # 🔥 YAHI PE (save back)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

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
            message=f"They selected {response.upper()}!"
        )
    else:
        return render_template(
            "status.html",
            status="waiting",
            message="Your crush has not responded yet ⏳"
        )

#---------------------------------------------------------------------------------------
# @app.route("/status/<unique_id>")
# def check_response(unique_id):
#     try:
#         with open(DATA_FILE, "r") as f:
#             data = json.load(f)
#     except json.JSONDecodeError:
#         data = {}

#     if unique_id in data:
#         response = data[unique_id].get("response")
#         if response:
#             return f"Your crush selected: {response.upper()} 💖"
#         else:
#             return "Your crush has not responded yet."
#     else:
#         return "Invalid link!"
#---------------------------------------------------------------------------------------
    

# ONE_WEEK = 7 * 24 * 60 * 60

# def clean_old_data(data):
#     current = time.time()
#     return {
#         k: v for k, v in data.items()
#         if current - v.get("created_at", current) < ONE_WEEK
#     }



if __name__ == "__main__":
    app.run()