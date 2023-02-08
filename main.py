from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# render_template()шаблонизатор т.е. в параметр этой функции передаём наименования html файлов, а саму функцию передаём в декоратор app.route()
# все htm файлы ПРИНЯТО хранить в подкаталоге templates

SQLAlchemy.SQLALCHEMY_TRACK_MODIFICATIONS = False
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # отключаем какуюто назойливую модификацию
db = SQLAlchemy(app)


# создаём класс для добавления записей в таблицу
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


# Создаём бд через терминал https://www.youtube.com/watch?v=G-si1WbtNeM&list=PL0lO_mIqDDFXiIQYjLbncE9Lb6sx8elKA&index=18

# теперь функционал для создания записей
@app.route('/create-article', methods=['POST', 'GET'])  # указали что функциия может обрабатывать данные
# с помощью функции POST. т.е. функция сможет обрабатывать данные из формы и прямой захд на страничку
def create_article():
    if request.method == 'POST':
        first = request.form['name']
        second = request.form['comment']

        article = Article(name=first, comment=second)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create-article.html')


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_article(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.name = request.form['name']
        article.comment = request.form['comment']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании записи произошла ошибка'
    else:

        return render_template('post_update.html', article=article)


@app.route('/posts')  # обработчик для вывода записей
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)  # то что красненьким это
    # наименование к которому мы сможем обращаться в шаблоне


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(
        id)  # функция для получения записи get_or_404 если не находит запись то выводит ошибку 404

    try:
        db.session.delete(article)  # Удаляем запись
        db.session.commit()  # Коммитим
        return redirect('/posts')
    except:
        return 'При удалении записи произошла ошибка'


# конструкция называется обработчик
@app.route('/')  # '/' означает гланую страницу, т.е. перейдя на главную страницу верни то что написано в return
def index():
    print(url_for('index'))  # т.е. ф-я url_for в качестве аргумента берёт название ф-ии
    # (сейчас index) и возвращает ассоциированный с ней url (сейчас "/"). Ну и чтобы протестить нада перейти на эту страницу (в нашем лучае на главную)
    # и в питоне в консоле вернётся "/". С помощью этого нам не придётся явно прописывать url что тупо как то и не динамочно и может привести к косякам
    return render_template('index.html')


# url_for('static', filename='css/style.css')  # а папка static находится в корне проекта рядом с templates

@app.route(
    '/profile/<string:username>')  # Такая структура означает, если мы будем переходить по адресу /profile/<тут какой угодно пользователь>, то страничка
# вернёт нам сообщение Пользователь <тут какой угодно пользователь>
def profile(username):
    return f'Пользователь {username}'


# with app.test_request_context(): # код для тестирования url_for()
#     print(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/video')
def video():
    return render_template('video_example.html')


@app.route('/qqq')
def qqq():
    return render_template('qqq.html')


# -------------------------------------------------------------
@app.route('/qwe')  # для примера для понимания
@app.route('/asd')
def primer():
    return 'primer!!!!!'


# условие для запуска сервера только на локальном устройстве
if __name__ == '__main__':
    app.run(debug=True)
