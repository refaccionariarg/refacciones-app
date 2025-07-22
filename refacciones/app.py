import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_FILE = 'refacciones.db'

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('q', '').lower()
    conn = get_connection()
    cur = conn.cursor()

    if query:
        cur.execute("SELECT * FROM refacciones WHERE LOWER(producto) LIKE ?", (f'%{query}%',))
    else:
        cur.execute("SELECT * FROM refacciones")
    
    refacciones = cur.fetchall()
    conn.close()
    return render_template('index.html', refacciones=refacciones, query=query)

@app.route('/agregar', methods=['POST'])
def agregar():
    producto = request.form['producto']
    modelo = request.form['modelo']
    marca = request.form['marca']
    sku = request.form['sku']
    precio = request.form['precio']
    cantidad = request.form['cantidad']

    conn = get_connection()
    conn.execute('INSERT INTO refacciones (producto, modelo, marca, sku, precio, cantidad) VALUES (?, ?, ?, ?, ?, ?)',
                 (producto, modelo, marca, sku, precio, cantidad))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = get_connection()
    conn.execute('DELETE FROM refacciones WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
