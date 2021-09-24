from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
print(datetime.utcnow)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buttonname.db'
db1 = SQLAlchemy(app)
class Buttonname(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    name = db1.Column(db1.Integer, nullable=False)
    buttonname = db1.Column(db1.Integer, nullable=False)
    deadline = db1.Column(db1.Integer, nullable=False)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        content = request.form['text']
        deadlineinfo = request.form['deadline']
        info = Buttonname(name=content,buttonname='False',deadline=deadlineinfo)
        try:
            db1.session.add(info)
            db1.session.commit()
            return redirect('/')
        except:
            return "There was an error in doing so"
    else:
        contents = Buttonname.query.order_by(Buttonname.id).all()
        return render_template("index1.html",contents=contents)

@app.route('/delete/<int:id>')
def delete_task(id):
    tasktobedeleted = Buttonname.query.get_or_404(id)
    try:
        db1.session.delete(tasktobedeleted)
        db1.session.commit()
        return redirect('/')
    except:
        return "There was an error in doing so."
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    task = Buttonname.query.get_or_404(id)
    if request.method == 'POST':
        cont = request.form['text']
        task.name = cont
        try:
            db1.session.commit()
            return redirect('/')
        except:
            return "There was an error in updating the task"
    else:
        return render_template('update1.html',task=task)

@app.route("/completed/<int:id>",methods=['GET','POST'])
def completed(id):
    button = Buttonname.query.get_or_404(id)
    if request.method == 'POST':
        button.buttonname = 'True'
        try:
            db1.session.commit()
            return redirect('/')
        except:
            return "There was an error in doing so"

@app.route("/updatedeadline/<int:id>",methods=['POST','GET'])
def updatedeadline(id):
    row = Buttonname.query.get_or_404(id)
    if request.method == 'POST':
        newdeadline = request.form['newdeadline']
        row.deadline = newdeadline
        try:
            db1.session.commit()
            return redirect('/')
        except:
            return "There was an error in doing so"
    else:
        return render_template('updatedeadline.html',row=row)


if __name__ == '__main__':
    app.run(debug=True)