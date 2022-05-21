from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
db = SQLAlchemy(app)

class ListForm(FlaskForm):
    to_do_input = StringField('Update todo', validators=[DataRequired()])
    submit = SubmitField('Update')

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get('title')

    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update_todo(todo_id):

    form = ListForm()
    if form.validate_on_submit():
        new_title = form.to_do_input.data

        todo = Todo.query.filter_by(id=todo_id).first()
        todo.title = new_title

        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", form=form)

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/done/<int:todo_id>")
def done(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/')
def index():

    todo_list = Todo.query.all()
    return render_template('index.html', todo_list= todo_list)




if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)