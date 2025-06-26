from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from models import Category

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Контент', validators=[DataRequired()])
    category = SelectField('Категорія', coerce=int)
    submit = SubmitField('Зберегти')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]
