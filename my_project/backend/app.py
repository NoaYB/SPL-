from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from models import db, User, Task
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'  # 

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Username already exists'}), 409

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'id': new_user.id, 'username': new_user.username}), 200

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # Assuming password is stored in plaintext for this example
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'msg': 'Invalid credentials'}), 401

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    description = data.get('description')


    # Check if description is provided
    if not description:
        return jsonify({'msg': 'Description is required'}), 400

    # Create and save the task
    new_task = Task(description=description,completed=False,user_id=get_jwt_identity())
    db.session.add(new_task)
    db.session.commit()
    print(description)

    # Return task details as per test expectations
    return jsonify({
        'id': new_task.id,
        'description': new_task.description,
        'completed': new_task.completed,
        'user_id': new_task.user_id
    }), 200

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.query.filter_by(user_id=get_jwt_identity()).all()
    tasks_list = [
        {
            'id': task.id,
            'description': task.description,
            'completed': task.completed,
            'user_id': task.user_id  
        }
        for task in tasks
    ]
    return jsonify(tasks_list), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get_or_404(task_id)

    if task.user_id != get_jwt_identity():
        return jsonify({'msg': 'Not authorized'}), 403

    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    db.session.commit()

    # Return the updated task details
    return jsonify({
        'id': task.id,
        'description': task.description,
        'completed': task.completed,
        'user_id': task.user_id
    }), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != get_jwt_identity():
        return jsonify({'message': 'Not authorized'}), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 
    app.run(debug=True, port=8000)  
