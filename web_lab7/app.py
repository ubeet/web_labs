from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, current_user
from flask_wtf import FlaskForm
from config import Config
from forms import NewsForm
from models import db, News, Category, User
from auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
@login_required
def add_news():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    form = NewsForm()
    if form.validate_on_submit():
        news = News(title=form.title.data, content=form.content.data, category_id=form.category.data)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form=form, action="Створити")

@app.route('/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
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
@login_required
def confirm_delete(news_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    form = DummyForm()
    news_item = News.query.get_or_404(news_id)
    if form.validate_on_submit():
        db.session.delete(news_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confirm_delete.html', news_item=news_item, form=form)

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin.html', users=users)
