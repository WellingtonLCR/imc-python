from flask import Flask, render_template, request, redirect, url_for, flash
from db import execute_query

app = Flask(__name__)
app.secret_key = 'imc_secret_key_2026'


def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)


def classificacao(imc):
    if imc < 18.5:
        return 'Abaixo do peso'
    elif imc < 25:
        return 'Peso normal'
    elif imc < 30:
        return 'Sobrepeso'
    elif imc < 35:
        return 'Obesidade grau 1'
    elif imc < 40:
        return 'Obesidade grau 2'
    return 'Obesidade grau 3'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resultados')
def resultados():
    try:
        sql = "SELECT * FROM calculos WHERE deletado_em IS NULL;"
        calculos = execute_query(sql, fetch=True) or []

        return render_template(
            'resultados.html',
            calculos=calculos,
            total=len(calculos),
            calcular_imc=calcular_imc,
            classificacao=classificacao
        )

    except Exception as e:
        flash('Erro ao buscar dados!', 'danger')
        app.logger.error(f'Erro no SELECT: {e}')
        return redirect(url_for('index'))


@app.route('/calcular', methods=['GET', 'POST'])
def calcular():
    if request.method == 'POST':
        try:
            nome = request.form.get('nome', '').strip()
            peso = float(request.form.get('peso'))
            altura = float(request.form.get('altura'))

            imc = calcular_imc(peso, altura)
            classif = classificacao(imc)

            sql = """
                INSERT INTO calculos(nome, peso, altura)
                VALUES(%s, %s, %s);
            """
            execute_query(sql, (nome, peso, altura))

            flash(f'{nome}, IMC: {imc} - {classif}', 'success')
            return redirect(url_for('resultados'))

        except ValueError:
            flash('Peso e altura devem ser números válidos.', 'danger')
            return redirect(url_for('calcular'))

        except Exception as e:
            flash('Erro ao salvar', 'danger')
            app.logger.error(f'Erro no INSERT: {e}')
            return redirect(url_for('calcular'))

    return render_template('formulario.html')


if __name__ == '__main__':
    app.run(debug=True)