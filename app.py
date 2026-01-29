from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os

# Create Flask app
app = Flask(__name__)

# Configure CORS to allow your frontend domain
# In production, replace '*' with your actual frontend URL
CORS(app)
# Sample data storage (in-memory)
# Note: In production, you should use a real database like PostgreSQL
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

tasks = [
    {"id": 1, "title": "Learn APIs", "completed": False},
    {"id": 2, "title": "Build a project", "completed": False}
]

# Home route
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the API!",
        "status": "online",
        "version": "1.0",
        "endpoints": {
            "GET /": "This help message",
            "GET /api/users": "Get all users",
            "GET /api/users/<id>": "Get a specific user",
            "POST /api/users": "Create a new user",
            "GET /api/tasks": "Get all tasks",
            "POST /api/tasks": "Create a new task",
            "PUT /api/tasks/<id>": "Update a task",
            "DELETE /api/tasks/<id>": "Delete a task",
            "GET /api/time": "Get current server time",
            "GET /health": "Health check endpoint"
        }
    })

# Health check endpoint (required by many hosting platforms)
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

# Get current time
@app.route('/api/time')
def get_time():
    return jsonify({
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": datetime.now().timestamp()
    })

# Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({
        "success": True,
        "count": len(users),
        "users": users
    })

# Get a specific user
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify({
            "success": True,
            "user": user
        })
    return jsonify({
        "success": False,
        "error": "User not found"
    }), 404

# Create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            "success": False,
            "error": "Name and email are required"
        }), 400
    
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    
    return jsonify({
        "success": True,
        "message": "User created successfully",
        "user": new_user
    }), 201

# Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        "success": True,
        "count": len(tasks),
        "tasks": tasks
    })

# Create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({
            "success": False,
            "error": "Title is required"
        }), 400
    
    new_task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "completed": data.get('completed', False)
    }
    tasks.append(new_task)
    
    return jsonify({
        "success": True,
        "message": "Task created successfully",
        "task": new_task
    }), 201

# Update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        return jsonify({
            "success": False,
            "error": "Task not found"
        }), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task['title'] = data['title']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    return jsonify({
        "success": True,
        "message": "Task updated successfully",
        "task": task
    })

# Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        return jsonify({
            "success": False,
            "error": "Task not found"
        }), 404
    
    tasks = [t for t in tasks if t["id"] != task_id]
    
    return jsonify({
        "success": True,
        "message": "Task deleted successfully"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    # Get port from environment variable (required for deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    # debug=False in production for security
    app.run(
        debug=os.environ.get('FLASK_ENV') == 'development',
        host='0.0.0.0',
        port=port
    )
