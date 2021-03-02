from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import DateField, SearchField

class QueryForm(FlaskForm):
    nombre = SearchField('Nombre')
    noid = SearchField('Numero de Identificacion')
    submit = SubmitField('Submit')
    fecha1 = DateField('Desde', validators=[validators.Optional()])
    fecha2 = DateField('Hasta', validators=[validators.Optional()])

class FlightForm(FlaskForm):
    id = SearchField('ICAO')
    submit = SubmitField('Submit')