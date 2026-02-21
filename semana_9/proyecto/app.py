from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gestion_productos')
def gestion_productos():
    return render_template('gestion_productos.html')

@app.route('/inventario')
def inventario():
    return render_template('Inventario.html')

if __name__ == '__main__':
    app.run(debug=True)