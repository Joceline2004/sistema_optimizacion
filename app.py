from flask import Flask, render_template
from algoritmo import ejecutar_algoritmo, evaluar_robustez

app = Flask(__name__)



@app.route('/')
def index():
    
    resultados = ejecutar_algoritmo()
    robustez = evaluar_robustez(5)

    return render_template(
        'index.html',
        resultados=resultados,
        robustez=robustez
    )


if __name__ == '__main__':
    app.run(debug=True)