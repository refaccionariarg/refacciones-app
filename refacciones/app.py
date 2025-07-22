import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from rapidfuzz import fuzz

app = Flask(__name__)
DB_FILE = 'refacciones.db'

# Lista fija de hojas (secciones)
hojas = [
    "ANTIIMPACTOS RG",
    "FAROS RG",
    "FACIAS",
    "SUSPEN-MECANICA",
    "CARROSERIA RG",
    "PUERTAS-COFRES"
]

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def buscar_fuzzy(query, refacciones):
    resultados = []
    palabras = query.lower().split()
    for ref in refacciones:
        texto = f"{ref['marca']} {ref['modelo']} {ref['producto']} {ref['No. SKU']}".lower()
        coincidencias = [fuzz.partial_ratio(p, texto) for p in palabras]
        if all(c >= 65 for c in coincidencias):  # Puedes ajustar el umbral
            resultados.append(ref)
    return resultados

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('q', '').strip().lower()
    hoja = request.args.get('hoja', None)  # Sección seleccionada
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT rowid AS id, * FROM refacciones")
    refacciones = cur.fetchall()
    conn.close()

    # Filtrar refacciones por sección en Python
    if hoja and hoja in hojas:
        hoja_lower = hoja.lower()
        refacciones = [r for r in refacciones if
                       hoja_lower in r['marca'].lower() or
                       hoja_lower in r['producto'].lower() or
                       hoja_lower in r['modelo'].lower()]

    # Filtro fuzzy para búsqueda
    if query:
        refacciones = buscar_fuzzy(query, refacciones)

    return render_template('index.html', refacciones=refacciones, query=query, hoja=hoja, hojas=hojas)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        producto = request.form['producto']
        modelo = request.form['modelo']
        marca = request.form['marca']
        sku = request.form['sku']
        precio = request.form['precio']
        cantidad = request.form['cantidad']

        conn = get_connection()
        conn.execute('INSERT INTO refacciones (producto, modelo, marca, `No. SKU`, precio, QTY) VALUES (?, ?, ?, ?, ?, ?)',
                     (producto, modelo, marca, sku, precio, cantidad))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('agregar.html', hojas=hojas)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = get_connection()
    conn.execute('DELETE FROM refacciones WHERE rowid = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
