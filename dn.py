from flask import Flask
from flask import render_template, redirect, url_for, flash
from forms import QueryForm, AuthenticateForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aurixbook'
Bootstrap(app)

import pandas as pd
import numpy as np

dn = pd.read_json('dn.json')

#Limpieza base de datos DNCD
dn['nacionalidad'] = dn['nacionalidad'].replace(to_replace='DOMINICANA ', value="República Dominicana")
dn['nacionalidad'] = dn['nacionalidad'].replace(to_replace='HOLANDA', value="Holanda") 

rowsTitle = ['divisione','inspectoria','seccion','apodo', 'nombre1', 'nombre2', 'apellido1', 'apellido2','sexo']
rowsCap = ['comentarios']
dn.fillna("",inplace=True)

for row in rowsTitle:
    dn[row] = dn[row].apply(lambda x : x.strip().title())

for row in rowsCap:
    dn[row] = dn[row].apply(lambda x : x.strip().capitalize())

rowsMerge = ['nombre1', 'nombre2', 'apellido1', 'apellido2']

dn['nombre'] = dn[rowsMerge[0]] + " " + dn[rowsMerge[1]] + " " \
                + dn[rowsMerge[2]] + " " + dn[rowsMerge[3]]

dn['nombre1'] = dn['nombre']
dn = dn.drop(columns=['nombre','nombre2', 'apellido1', 'apellido2'])
dn = dn.rename(columns={'nombre1': 'nombre'})

@app.route('/')
@app.route('/dashboard')
def dashboard():
    ## Grafico Presos Por Mes
    grouped1 = dn.groupby(['anio','mes'])['detenidoId']
    groups1 = grouped1.groups
    labels1 = []
    for idx in groups1:
        labels1.append(str(idx))
    values1 = grouped1.count().values.tolist()
    legend1 = "Cronologico de Cantidad de Detenidos (2004-)"

    ## Grafico Averaje por Mes
    grouped2 = dn.groupby('mes')['detenidoId']
    groups2 = grouped2.groups
    labels2 = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio','Agosto', 'Septiembre','Octubre', 'Noviembre', 'Diciembre']
    values2 = grouped2.count()/len(dn['anio'].unique())
    legend2 = "Averaje de Detenidos Cada Mes"

    ##Grafico Cantidad Por Nacionalidad (Extranjeros)
    filtroRD = dn[(dn['nacionalidad']!='República Dominicana') & (dn['nacionalidad']!='')]
    extranjeros = filtroRD.groupby('nacionalidad')['detenidoId']
    labels3 = extranjeros.count().reset_index(name='count')\
                            .sort_values(['count'], ascending=False)['nacionalidad']\
                            .values.tolist()    
    values3 = extranjeros.count().reset_index(name='count')\
                            .sort_values(['count'], ascending=False)['count']\
                            .values.tolist()
    legend3 = "Cantidad por Nacionalidad (Extranjeros)"

    return render_template('dashboard.html', 
    legend1=legend1, values1=values1, labels1=labels1,
    legend2=legend2, values2=values2, labels2=labels2,
    legend3=legend3, values3=values3, labels3=labels3,
    )


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = QueryForm()
    if form.validate_on_submit():
        noid = form.noid.data.strip()
        nombre = form.nombre.data.strip()

        classes = ["table", "table-dark", "table-hover", "table-striped"]

        if noid and nombre:
            flash('We support queries accross single features only. In this case ID String takes precedent')

        if noid:
            form.nombre.data = None
            rnoid = dn[dn['numeroIdentificacion'].str.contains(noid, na=False, case=False)]            
            return render_template('query.html', form=form, condition=rnoid.to_html(classes=classes))

        if nombre:
            form.noid.data = None
            rnombre = dn[np.logical_and.reduce([dn['nombre'].str.contains(word, na=False, case=False) for word in nombre.split()])]
            return render_template('query.html', form=form, condition=rnombre.to_html(classes=classes))

        else:
            flash('Please provide at least one field to query our database')
            return render_template('query.html', form=form)
            
    return render_template('query.html', form=form)
