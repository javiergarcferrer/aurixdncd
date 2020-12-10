from flask import Flask
from flask import render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from forms import QueryForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aurixbook'
Bootstrap(app)

import pandas as pd
dn = pd.read_json('dn.json')

#Limpieza de base de datos de la DNCD
dn['nacionalidad'] = dn['nacionalidad'].replace(to_replace='DOMINICANA ', value="República Dominicana")
dn['nacionalidad'] = dn['nacionalidad'].replace(to_replace='HOLANDA', value="Holanda") 

@app.route('/')
@app.route('/index')
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
    labels2 = ['Enero', 'Febrero', 'Marzo', 'Abril',       'Mayo', 'Junio', 'Julio','Agosto', 'Septiembre','Octubre', 'Noviembre', 'Diciembre']
    values2 = grouped2.count()/len(dn['anio'].unique())
    legend2 = "Averaje de Detenidos Cada Mes"

    ##Grafico Cantidad Por Nacionalidad (Extranjeros)
    filtroRD = dn[dn['nacionalidad']!='República Dominicana']
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
        nombre1 = form.nombre1.data
        apellido1 = form.apellido1.data
        
        rnombre1 = dn[dn['nombre1'].str.contains(nombre1, na=False, case=False)]
        rapellido1 = dn[dn['apellido1'].str.contains(apellido1, na=False, case=False)]
        
        combined = rnombre1[rnombre1['apellido1'].str.contains(apellido1, na=False, case=False)]

        if nombre1 and apellido1:
            return render_template('query.html', form=form, combined=combined.to_html())

        elif nombre1:
            return render_template('query.html', form=form, rnombre1=rnombre1.to_html()) 

        elif apellido1:
            return render_template('query.html', form=form, rapellido1=rapellido1.to_html())
        
        else:
            flash('Please provide at least one field to query our database')
            return render_template('query.html', form=form)
    return render_template('query.html', form=form)