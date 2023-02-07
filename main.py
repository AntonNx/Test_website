from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

# render_template()шаблонизатор т.е. в параметр этой функции передаём наименования html файлов, а саму функцию передаём в декоратор app.route()
# все htm файлы ПРИНЯТО хранить в подкаталоге templates

SQLAlchemy.SQLALCHEMY_TRACK_MODIFICATIONS=False
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    comment = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Client {self.id} {self.name} {self.date} {self.comment}>'


db.create_all()

clients1 = Client.query.all()




@app.route('/clients', methods=['POST'])
def create_client():
    name = request.form['name']
    date = request.form['date']
    comment = request.form['comment']
    client = Client(name=name, date=date, comment=comment)
    db.session.add(client)
    db.session.commit()
    return f'Client {client.name} with id {client.id}  created'

for client in clients1:
    print("Name: ", client.name)
    print("Date: ", client.date)
    print("Comment: ", client.comment)
# db.drop_all()

# конструкция называется обработчик
@app.route('/')  # '/' означает гланую страницу, т.е. перейдя на главную страницу верни то что написано в return
def index():
    print(url_for('index'))  # т.е. ф-я url_for в качестве аргумента берёт название ф-ии
    # (сейчас index) и возвращает ассоциированный с ней url (сейчас "/"). Ну и чтобы протестить нада перейти на эту страницу (в нашем лучае на главную)
    # и в питоне в консоле вернётся "/". С помощью этого нам не придётся явно прописывать url что тупо как то и не динамочно и может привести к косякам
    return render_template('index.html')


# url_for('static', filename='css/style.css')  # а папка static находится в корне проекта рядом с templates

@app.route('/profile/<string:username>')  # Такая структура означает, если мы будем переходить по адресу /profile/<тут какой угодно пользователь>, то страничка
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

