from flask import Flask
from flask import render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from forms import QueryForm, AuthenticateForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aurixbook'
Bootstrap(app)

import pandas as pd
dn = pd.read_json('dn.json')

#Limpieza base de datos DNCD
dn['nacionalidad'] = dn['nacionalidad'].replace(to_replace='DOMINICANA ', value="República Dominicana")
dn['nacionalidad'] = dn['nacionalidad'].replace(to_replace='HOLANDA', value="Holanda") 

#def login():
#    form = AuthenticateForm()
#    if form.validate_on_submit:
#        key = form.key.data
#        if key == "jochi2024":
#            return redirect(url_for('dashboard'))
#    else:
#        flash('Wrong key input')
#    return render_template('login.html', form=form)

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
        noid = form.noid.data

        nombre1 = form.nombre1.data
        apellido1 = form.apellido1.data
        nombre2 = form.nombre2.data
        apellido2 = form.apellido2.data
        
        rnoid = dn[dn['numeroIdentificacion'].str.contains(noid, na=False, case=False)]

        rnombre1 = dn[dn['nombre1'].str.contains(nombre1, na=False, case=False)]
        rapellido1 = dn[dn['apellido1'].str.contains(apellido1, na=False, case=False)]
        rnombre2 = dn[dn['nombre2'].str.contains(nombre2, na=False, case=False)]
        rapellido2 = dn[dn['apellido2'].str.contains(apellido2, na=False, case=False)]
        
        n1a1 = rnombre1[rnombre1['apellido1'].str.contains(apellido1, na=False, case=False)]
        n1n2a1 = n1a1[n1a1['nombre2'].str.contains(nombre2, na=False, case=False)]
        combined = n1n2a1[n1n2a1['apellido2'].str.contains(apellido2, na=False, case=False)]

        classes = ["table", "table-dark", "table-hover", "table-striped"]

        if noid:
            return render_template('query.html', form=form, condition=rnoid.to_html(classes=classes))

        elif nombre1 and apellido1 and nombre2 and apellido2:
            return render_template('query.html', form=form, condition=combined.to_html(classes=classes))

        elif nombre1 and apellido1 and not nombre2 and not apellido2:
            return render_template('query.html', form=form, condition=n1a1.to_html(classes=classes))

        elif nombre1:
            return render_template('query.html', form=form, condition=rnombre1.to_html(classes=classes)) 

        elif apellido1:
            return render_template('query.html', form=form, condition=rapellido1.to_html(classes=classes))
        
        else:
            flash('Please provide at least one field to query our database')
            return render_template('query.html', form=form)
    return render_template('query.html', form=form)
