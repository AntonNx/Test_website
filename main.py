import sqlalchemy
from flask import Flask, render_template, url_for
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2

# render_template()шаблонизатор т.е. в параметр этой функции передаём наименования html файлов, а саму функцию передаём в декоратор app.route()
# все htm файлы ПРИНЯТО хранить в подкаталоге templates
app = Flask(__name__)

# Устанавливаем соединение с postgres
connection = psycopg2.connect(user="postgres", password="123")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Создаем курсор для выполнения операций с базой данных
cursor = connection.cursor()

# Создаем базу данных
try:
    sql_create_database = cursor.execute('create database sqlalchemy_tuts')
except:
    l = 1
metadata = sqlalchemy.MetaData()

clients = sqlalchemy.Table('clients', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('client', sqlalchemy.String(300), primary_key=False),
    sqlalchemy.Column('Bolezn', sqlalchemy.String(900), primary_key=False),
    sqlalchemy.Column('date', sqlalchemy.DateTime, primary_key=False, default=datetime.utcnow())
)
metadata.create_all(clients)
# Закрываем соединение
cursor.close()
connection.close()


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


@app.route('/qwe')  # для примера для понимания
@app.route('/asd')
def primer():
    return 'primer!!!!!'


# условие для запуска сервера только на локальном устройстве
if __name__ == '__main__':
    app.run(debug=True)
