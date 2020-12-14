from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    nombre1 = StringField('Nombre')
    nombre2 = StringField('Segundo Nombre')
    apellido1 = StringField('Apellido')
    apellido2 = StringField('Segundo Apellido')
    noid = StringField('Numero de Identificacion')
    submit = SubmitField('Submit')

class AuthenticateForm(FlaskForm):
    key = StringField('Secret Key')