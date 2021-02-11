from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class QueryForm(FlaskForm):
    nombre = StringField('Nombre')
    noid = StringField('Numero de Identificacion')
    submit = SubmitField('Submit')

class FlightForm(FlaskForm):
    id = StringField('ID')
    submit = SubmitField('Submit')