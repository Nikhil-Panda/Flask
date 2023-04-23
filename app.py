from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()
    for table in db.Model.metadata.tables.values():
        print(table.name)

@app.route('/',methods=['POST','GET']) #for the index page
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue in adding the task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_del = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting it."

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task_update = Todo.query.get_or_404(id)
    #till we dont click the update button, update.html is visible to us.
    if request.method == "POST":
        task_update.content = request.form['content']
        # updated = Todo(content = task_update) not required since
        #we already added the content to task_update above.

        try:
            # db.session.add(updated), same as above
            db.session.commit()
            return redirect('/')
        except:
            return "Task could not be updated"
    else:
        return render_template('update.html', task_update=task_update)
    

