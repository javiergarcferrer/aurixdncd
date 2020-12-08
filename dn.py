from flask import Flask
from flask import render_template
app = Flask(__name__)

import pandas as pd

@app.route('/')
def dashboard():
    dn = pd.read_json('dn.json')
    ## Grafico Presos Por Mes
    grouped1 = dn.groupby(['anio','mes'])['detenidoId']
    groups1 = grouped1.groups
    labels1 = []
    for idx in groups1:
        labels1.append(str(idx))
    values1 = grouped1.count().values.tolist()
    legend1 = "Presos Por Mes"

    ## Grafico Averaje por Mes
    grouped2 = dn.groupby(['mes'])['detenidoId']
    groups2 = grouped2.groups
    labels2 = []
    for idx in groups2:
        labels2.append(str(idx))
    values2 = grouped2.mean().values.tolist()
    legend2 = "Averaje Por Mes"

    return render_template('dashboard.html', 
    legend1=legend1, values1=values1, labels1=labels1,
    legend2=legend2, values2=values2, labels2=labels2
    )