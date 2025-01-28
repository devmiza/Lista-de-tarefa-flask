from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#Definindo um modelo de dados
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), unique=True, nullable=False)
    completed = db.Column(db.Boolean, default=False)

#cRud (Read)
@app.route('/')
def index():
    all_tasks = Tasks.query.all()
    pending_tasks = Tasks.query.filter_by(completed=False).all()
    completed_tasks = Tasks.query.filter_by(completed=True).all()
    return render_template('base.html', all_tasks=all_tasks, pending_tasks=pending_tasks, completed_tasks=completed_tasks)

#Crud (Create)
@app.route('/create', methods=['POST'])
def create_task():
    description = request.form['description']
    description = description.upper()

    #Valida se a tarefa já existe
    existind_task = Tasks.query.filter_by(description=description).first()
    if existind_task:
        return 'Tarefa já cadastrada!', 400

    new_task = Tasks(description = description)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

# #crUd (Update)
# @app.route('/update/<int:task_id>', methods=['POST'])
# def update_task(task_id):
#     task = Tasks.query.get(task_id)

#     if task:
#         task.description = request.form['description']
#         task.description = task.description.upper()
#         db.session.commit()
#     return redirect('/')

# #cruD (Delete)
# @app.route('/delete/<int:task_id>', methods=['POST'])
# def delete_task(task_id):
#     task = Tasks.query.get(task_id)

#     if task:
#         db.session.delete(task)
#         db.session.commit()
#     return redirect('/')

# Atualizar ou Deletar
@app.route('/update_or_delete/<int:task_id>', methods=['POST'])
def update_or_delete_task(task_id):
    task = Tasks.query.get(task_id)
    if task:
        if request.form['action'] == 'edit':
            task.description = request.form['description']
            task.description = task.description.upper()
            db.session.commit()
        elif request.form['action'] == 'delete':
            db.session.delete(task)
            db.session.commit()
    return redirect('/')

# Atualizar Status
@app.route('/toggle_status/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    task = Tasks.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5153)