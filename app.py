from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS

app.secret_key = "super_clave_secreta_de_daniel"

# 🔑 API de OpenAI
client = OpenAI(api_key="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")

# 🧑 Usuario de ejemplo
USUARIO = {
    "username": "daniel",
    "password": "1234"
}

# 🏠 Página principal
@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["username"])

# 🔐 Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USUARIO["username"] and password == USUARIO["password"]:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="User or password incorrect")

    return render_template("login.html")

# 🚪 Logout (versión unificada)
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))



# 🤖 Endpoint de IA
@app.route("/ask", methods=["POST"])
def ask():
    if "username" not in session:
        return jsonify({"error": "You should log in to use the AI."}), 403

    data = request.get_json()
    user_input = data.get("prompt", "")
    prompt = f"Respond to the following message just in english: {user_input}"

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert assistant for improving resumes and job applications."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
