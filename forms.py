from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    nombre = StringField('Nombre')
    noid = StringField('Numero de Identificacion')
    submit = SubmitField('Submit')

class AuthenticateForm(FlaskForm):
    key = StringField('Secret Key')