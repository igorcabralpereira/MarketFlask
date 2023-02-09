from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Usuário já existe, Favor tente novamente com outro Usuário.')

    def validate_email_endereco(self, email_endereco_to_check):
        email_endereco = User.query.filter_by(email=email_endereco_to_check.data)
        if email_endereco:
            raise ValidationError('E-mail já existe, Favor tente novamente com outro endereço de E-mail.')

    username = StringField(label='Usuário: ', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='E-mail: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Senha: ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirme a senha: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Cadastrar')


class LoginForm(FlaskForm):
    username = StringField(label='Usuário', validators=[DataRequired()])
    password = PasswordField(label='Senha: ', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class ComprarItemForm(FlaskForm):
    submit = SubmitField(label='Comprar Item!')


class VenderItemForm(FlaskForm):
    submit = SubmitField(label='Vender Item!')
