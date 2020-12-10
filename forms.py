from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    nombre1 = StringField('Nombre')
    apellido1 = StringField('Apellido')
    submit = SubmitField('Submit')