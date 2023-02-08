from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(80), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Record(client='{self.client}', comment='{self.comment}', date='{self.date}')"


db.create_all()


@app.route('/record', methods=['POST'])
def insert_record():
    record = Record(client=request.form['client'], comment=request.form['comment'], date=request.form['date'])
    db.session.add(record)
    db.session.commit()
    return "Record added."


@app.route('/records', methods=['GET'])
def retrieve_records():
    records = Record.query.all()
    return str(records)


if __name__ == '__main__':
    app.run(debug=True)