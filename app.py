from datetime import datetime
from os import error
from flask import Flask,render_template,request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(200), unique=True, nullable=False)
    date_time = db.Column(db.DateTime, unique=True, default = datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title} - {self.desc} - {self.date_time}"

@app.route("/",methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        titel = request.form['title']
        decs = request.form['desc']
        todo = Todo(title=titel,desc=decs)
        db.session.add(todo)
        db.session.commit()
        all = Todo.query.all()
        return render_template('main.html',allTodo=all)    
    elif request.method == 'GET':
        all = Todo.query.all()
        return render_template('main.html',allTodo=all)
    return 404
@app.route("/delete/<int:sno>")
def delete(sno):
      todo = Todo.query.filter_by(sno=sno).first()
      db.session.delete(todo)
      db.session.commit()
      return redirect('/')

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        todo = Todo.query.filter_by(sno=sno).first()
        title = request.form['title'] 
        desc = request.form['desc']
        todo.title=title
        todo.desc = desc 
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    elif request.method == 'GET':
        todo = Todo.query.filter_by(sno=sno).first()
        return render_template('update.html',todo=todo)
if __name__ == "__main__":  
    app.run()