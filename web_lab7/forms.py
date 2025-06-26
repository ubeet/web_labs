from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from models import Category

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Контент', validators=[DataRequired()])
    category = SelectField('Категорія', coerce=int)
    submit = SubmitField('Зберегти')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]

class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')

class RegisterForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Підтвердження', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Адміністратор')
    submit = SubmitField('Зареєструватися')
