# app.py
from flask import Flask, request, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)

INTEGRANTES = [
    {"nombre": "Arnold Minano", "password": "AMredes26"},
    {"nombre": "Sebastian Pino", "password": "SPredes26"}
]

def init_db():
    db_path = "usuarios.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  password_hash TEXT NOT NULL)''')
    for user in INTEGRANTES:
        hash_pass = generate_password_hash(user["password"])
        c.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)",
                  (user["nombre"], hash_pass))
    conn.commit()
    conn.close()
    print("Base de datos creada con hashes.")

init_db()

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Validacion DRY7122</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f4f4f9; }
        .container { max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; }
        input[type=text], input[type=password] { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; }
        input[type=submit] { background: #007bff; color: white; padding: 10px; border: none; cursor: pointer; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Validacion de Integrantes</h2>
        <form method="POST">
            <label>Nombre:</label>
            <input type="text" name="username" required>
            <label>Contrasena:</label>
            <input type="password" name="password" required>
            <input type="submit" value="Validar">
        </form>
        {% if mensaje %}
            <p class="{{ 'success' if exito else 'error' }}">{{ mensaje }}</p>
        {% endif %}
        <hr><small>Puerto 5800 - Examen DRY7122</small>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def validar_usuario():
    mensaje = ""
    exito = False
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            conn = sqlite3.connect('usuarios.db')
            c = conn.cursor()
            c.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (username,))
            resultado = c.fetchone()
            conn.close()
            if resultado and check_password_hash(resultado[0], password):
                mensaje = f"Bienvenido {username}!"
                exito = True
            else:
                mensaje = "Usuario o contrasena incorrectos."
        else:
            mensaje = "Complete todos los campos."
    return render_template_string(HTML_FORM, mensaje=mensaje, exito=exito)

if __name__ == '__main__':
    print("Servidor en http://127.0.0.1:5800")
    app.run(host='0.0.0.0', port=5800, debug=True)
