from flask import Flask, render_template
from algoritmo import ejecutar_algoritmo

app = Flask(__name__)

app = Flask(__name__)

@app.route('/')
def index():

    resultados = ejecutar_algoritmo()

    return render_template(
        'index.html',
        resultados=resultados
    )


if __name__ == '__main__':
    app.run(debug=True)