from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from chatbot_logic import get_chatbot_response
from database.database import create_tables, connect_db
import joblib

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Ensure database tables exist
create_tables()

# Load model if exists
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "depression_rf_model.pkl")
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

# ----------------- HOME -----------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ----------------- REGISTER -----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",(name,email,password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except Exception as e:
            conn.close()
            return render_template("register.html", error=str(e))
    return render_template("register.html")

# ----------------- LOGIN -----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user'] = user[1]
            session['user_email'] = user[2]
            return redirect(url_for('personal_info'))
        else:
            return render_template("login.html", error="Invalid email or password!")
    return render_template("login.html")

# ----------------- PERSONAL INFO -----------------
@app.route('/personal_info', methods=['GET','POST'])
def personal_info():
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['age'] = request.form.get('age')
        session['gender'] = request.form.get('gender', 'male').lower()
        session['occupation'] = request.form.get('occupation')
        session['department'] = request.form.get('department')
        session['academic_year'] = request.form.get('academic_year')
        session['cgpa'] = request.form.get('cgpa')
        session['scholarship'] = request.form.get('scholarship')
        return redirect(url_for('questionnaire'))

    return render_template("personal_info.html", name=session.get('user'))

# ----------------- QUESTIONNAIRE -----------------
QUESTIONS = [
    "I feel sad or down.",
    "I have lost interest in daily activities.",
    "I feel tired or have low energy.",
    "I have trouble sleeping or sleep too much.",
    "I feel guilty or worthless.",
    "I have difficulty concentrating.",
    "I feel anxious or restless.",
    "I avoid social activities.",
    "I feel hopeless about the future."
]

@app.route("/questionnaire", methods=["GET","POST"])
def questionnaire():
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        responses = [int(request.form.get(f"q{i+1}",0)) for i in range(9)]
        age = float(session.get('age',18))
        gender = 0 if session.get('gender','male')=='male' else 1
        cgpa = float(session.get('cgpa',0.0))
        features = [age, gender, 0, cgpa] + responses
        prediction = model.predict([features])[0] if model else "Model not found"
        message = f"Predicted Depression Level: {prediction}"
        return render_template("result.html", message=message, name=session.get('user'))

    return render_template("questionnaire.html", name=session.get('user'), questions=QUESTIONS)

# ----------------- CHATBOT -----------------
@app.route('/chatbot')
def chatbot_page():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("chatbot.html", name=session.get('user'))

@app.route("/chatbot_api", methods=["POST"])
def chatbot_api():
    if not session.get("user"):
        return jsonify({"response":"Please login first."})
    user_msg = request.json.get("message","")
    response = get_chatbot_response(user_msg)
    return jsonify({"response": response})

# ----------------- LOGOUT -----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

# ----------------- RUN SERVER -----------------
if __name__ == "__main__":
    app.run(debug=True)
