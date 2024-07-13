from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, PasswordField
from wtforms.validators import DataRequired, InputRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    hashed_password = PasswordField('Пароль', validators=[DataRequired(), InputRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    hashed_password = PasswordField('Пароль', validators=[DataRequired(), InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')