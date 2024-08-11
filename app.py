from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Creating database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'
db = SQLAlchemy(app)

# Table definition
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>'  % self.id
    
with app.app_context():
        db.create_all()

# Output table

@app.route('/', methods=['POST', 'GET'])
def index():
    tasks = ToDo.query.order_by(ToDo.date_created).all() # get all rows
    return render_template('index.html', tasks=tasks) # put table as a var to template

# Adding data

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error with database.'
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)

# Delete

@app.route('/del/<int:id>', methods=['POST', 'GET'])
def dell(id):
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Error with deleting."
     
# Update(Sql update)   
        
@app.route('/compl/<int:id>', methods=['POST', 'GET'])
def compl(id):
    try:
        task_to_complete = ToDo.query.get_or_404(id)
        task_to_complete.completed = not task_to_complete.completed
        db.session.commit()
        return redirect('/')
    except:
        return "Error with compliting"
    
    
@app.route('/upd/<int:id>', methods=['POST', 'GET'])
def upd(id):
    task_to_update = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error with updating"
    else:
        return render_template('update.html', task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)