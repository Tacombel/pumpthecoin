from flask import flash, redirect, render_template, session, url_for

from app import app
from app.forms import palabra_en_formacion
import siguiente_letra


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = palabra_en_formacion()
    if 'letras' in session:
        letras_old = session['letras']
    else:
        letras_old = ''
        session['letras'] = letras_old
    if 'candidatas' in session:
        candidatas = session['candidatas']
    else:
        candidatas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if form.validate_on_submit():
        candidatas = []
        letra = form.letras.data
        letra = letra.lower()
        letras = letras_old + letra
        letras = letras.upper()
        candidatas_lower = siguiente_letra.main(letras.lower())
        for e in candidatas_lower:
            candidatas.append(e.upper())
        session['letras'] = letras
        session['candidatas'] = candidatas
        return redirect(url_for('index'))
    return render_template('index.html', form=form, letras=session['letras'], candidatas=candidatas)

@app.route('/reset')
def reset():
    session['letras'] = ''
    session['candidatas'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    return redirect(url_for('index'))
