from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        mydata = Todo(title=title, desc=desc)
        db.session.add(mydata)
        db.session.commit()

    allmydata = Todo.query.all()
    
    
    return render_template('index.html', allmydata=allmydata)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        mydata = Todo.query.filter_by(sno=sno).first()
        mydata.title = title
        mydata.desc = desc
        db.session.add(mydata)
        db.session.commit()
        return redirect('/')

    mydata = Todo.query.filter_by(sno=sno).first()
    
    return render_template('update.html', mydata=mydata)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    mydata = Todo.query.filter_by(sno=sno).first()
    db.session.delete(mydata)
    db.session.commit()
    return redirect("/")


@app.route('/show')
def show():
    allmydata = Todo.query.all()
    print(allmydata)
    return "this is a query page"


if __name__ == "__main__":
    app.run(debug=True, port=8000)