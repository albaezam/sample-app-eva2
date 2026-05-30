from flask import Flask, request
import sqlite3

app = Flask(__name__)

def inicializar_bd():
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        nombre TEXT,
        password TEXT
    )
    ''')

    conexion.commit()
    conexion.close()

@app.route('/', methods=['GET', 'POST'])
def inicio():

    usuario = request.values.get('usuario')
    password = request.values.get('password')

    if usuario and password:

        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nombre, password) VALUES (?, ?)",
            (usuario, password)
        )

        conexion.commit()

        cursor.execute(
            "SELECT * FROM usuarios WHERE nombre=? AND password=?",
            (usuario, password)
        )

        cuenta = cursor.fetchone()

        conexion.close()

        if cuenta:
            return f"Validación Exitosa: Bienvenido {usuario}.\n"

        else:
            return "Error: Credenciales inválidas.\n"

    return "Servidor Flask operativo en puerto 5000.\n"

if __name__ == '__main__':
    inicializar_bd()
    app.run(host='0.0.0.0', port=5000)

