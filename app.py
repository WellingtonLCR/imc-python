from flask import Flask, render_template, request, redirect, url_for, flash
from db import execute_query

app = Flask(__name__)
app.secret_key = 'imc_secret_key_2026'


@app.route('/')
def index():
    sql = "SHOW TABLES;"
    resultados = execute_query(sql, fetch=True)
    print(resultados)
    return render_template('index.html')


@app.route('/resultados')
def resultados():
    calculos = []
    return render_template('resultados.html', calculos=calculos, total=len(calculos))


@app.route('/calcular', methods=['GET', 'POST'])
def calcular():
    if request.method == 'POST':
        nome = request.form.get('nome', 'Não foi enviado um nome')
        peso = request.form.get('peso')
        altura = request.form.get('altura')

        try:
            peso = float(peso)
            altura = float(altura)

            imc = round(peso / (altura ** 2), 2)

            if imc < 18.5:
                classificacao = 'Abaixo do peso'
            elif imc < 25:
                classificacao = 'Peso normal'
            elif imc < 30:
                classificacao = 'Sobrepeso'
            elif imc < 35:
                classificacao = 'Obesidade grau 1'
            elif imc < 40:
                classificacao = 'Obesidade grau 2'
            else:
                classificacao = 'Obesidade grau 3'

            flash(
                f'Olá {nome}, seu IMC é: {imc} - Classificação: {classificacao}',
                'success'
            )

            return redirect(url_for('resultados'))

        except ValueError:
            flash('Peso e altura devem ser números válidos.', 'danger')
            return redirect(url_for('calcular'))

    return render_template('formulario.html')


if __name__ == '__main__':
    app.run(debug=True)