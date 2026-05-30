from flask import Flask, jsonify, request
import random
import string
import sqlite3

app = Flask(__name__)

# BASE DE DATOS
conn = sqlite3.connect('usuarios.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
''')
conn.commit()

# TOKEN RANDOM
@app.route('/token', methods=['GET'])
def token():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return jsonify({"token": token})

# RED FISICA
@app.route('/red', methods=['GET'])
def red():
    return jsonify({
        "router": "Cisco",
        "switch": "Catalyst 2960",
        "firewall": "ASA5505"
    })

# CREAR USUARIO
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():

    data = request.json

    username = data['username']
    password = data['password']

    cursor.execute(
        "INSERT INTO usuarios (username,password) VALUES (?,?)",
        (username,password)
    )

    conn.commit()

    return jsonify({"mensaje":"Usuario creado correctamente"})


if __name__ == '__main__':
    app.run(debug=True)
