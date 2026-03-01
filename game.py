from flask import Flask, jsonify, render_template, request
import random

app = Flask(__name__)

EMOJIS = [
    "🐸", "🐶", "🐱", "🦊", "🐼", "🐵", "🦄", "🐙", "🐢", "🐝",
    "🦋", "🐞", "🐰", "🐯", "🦁", "🐷", "🐨", "🐤", "🦕", "🌟",
]

score = 0
current_target = None
current_choices = []


def generate_round():
    global current_target, current_choices
    current_target = random.choice(EMOJIS)
    others = [emoji for emoji in EMOJIS if emoji != current_target]
    current_choices = random.sample(others, 8) + [current_target]
    random.shuffle(current_choices)


def state_payload():
    if current_target is None or len(current_choices) != 9:
        generate_round()
    return {
        "score": score,
        "target": current_target,
        "choices": current_choices,
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/state")
def state():
    return jsonify(state_payload())


@app.post("/click")
def click():
    global score

    data = request.get_json(silent=True) or {}
    clicked = data.get("emoji", "")
    correct = clicked == current_target

    if correct:
        score += 1
        message = "Correct!"
    else:
        message = "Try again!"

    generate_round()

    return jsonify(
        {
            "correct": correct,
            "score": score,
            "message": message,
            "target": current_target,
            "choices": current_choices,
        }
    )


@app.post("/reset")
def reset():
    global score
    score = 0
    generate_round()
    return jsonify(state_payload())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
