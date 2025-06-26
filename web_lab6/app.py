from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import HiddenField
from forms import NewsForm
from models import db, News, Category

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

class DummyForm(FlaskForm):
    pass

@app.route('/')
def index():
    news = News.query.all()
    return render_template('index.html', news_list=news)

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    news_item = News.query.get_or_404(news_id)
    return render_template('detail.html', news_item=news_item)

@app.route('/add', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(title=form.title.data, content=form.content.data, category_id=form.category.data)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form=form, action="Створити")

@app.route('/edit/<int:news_id>', methods=['GET', 'POST'])
def edit_news(news_id):
    news = News.query.get_or_404(news_id)
    form = NewsForm(obj=news)
    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        news.category_id = form.category.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form=form, action="Редагувати")

@app.route('/delete/<int:news_id>/confirm', methods=['GET', 'POST'])
def confirm_delete(news_id):
    form = DummyForm()
    news_item = News.query.get_or_404(news_id)
    if form.validate_on_submit():
        db.session.delete(news_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confirm_delete.html', news_item=news_item, form=form)

if __name__ == '__main__':
    app.run(debug=True)
