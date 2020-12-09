from flask import Flask
from flask import url_for, render_template, request, redirect
#from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    language = db.Column(db.Text)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Text)
    q2 = db.Column(db.Integer)

@app.route('/')
def instruction():
    return render_template('first.html')

@app.route('/survey')
def survey():
    survey = Questions.query.all()
    return render_template(
        'survey.html',
        survey=survey
    )

@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('survey'))
    age = request.args.get('age')
    language = request.args.get('language')
    user = User(
        age=age,
        language=language
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    q1 = request.args.get('food')
    q2 = request.args.get('finger')

    answer = Answers(id=user.id, q1=q1, q2=q2)
    db.session.add(answer)
    db.session.commit()
    return 'Ok'

@app.route('/stats')
def stats():
    return render_template('stats.html')

if __name__ == '__main__':
    app.run(debug=True)