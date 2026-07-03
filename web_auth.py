# web_auth.py
import sqlite3
from flask import Flask, request, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Nombres de integrantes 
INTEGRANTES = [
    "Arnold Minano",
    "Sebastian Pino"
    
]

CONTRASENAS = {
    "Arnold Minano": "arnoldm123",
    "Sebastian Pino": "Sebap456"
    
}

def init_db():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT UNIQUE,
                  password_hash TEXT)''')
    # Insertar integrantes si no existen
    for nombre in INTEGRANTES:
        # Verificar si ya existe
        c.execute("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
        if c.fetchone() is None:
            hash_pass = generate_password_hash(CONTRASENAS[nombre])
            c.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, hash_pass))
    conn.commit()
    conn.close()

# Página de login simple (HTML embebido)
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Ingreso de Usuarios</h2>
    <form method="post">
        <label>Usuario: <input type="text" name="username"></label><br>
        <label>Contraseña: <input type="password" name="password"></label><br>
        <input type="submit" value="Iniciar sesión">
    </form>
    {% if mensaje %}
        <p>{{ mensaje }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('usuarios.db')
        c = conn.cursor()
        c.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row:
            hash_pass = row[0]
            if check_password_hash(hash_pass, password):
                mensaje = f"Bienvenido {username}, autenticación exitosa."
            else:
                mensaje = "Contraseña incorrecta."
        else:
            mensaje = "Usuario no encontrado."
    return render_template_string(LOGIN_HTML, mensaje=mensaje)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5800, debug=True)
