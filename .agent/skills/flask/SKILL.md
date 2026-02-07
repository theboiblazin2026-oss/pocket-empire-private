---
name: Flask
description: Minimal Python, blueprints, extensions, Jinja templates
---

# Flask Skill

## Basic App

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Hello!'})

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.json
        return jsonify(data), 201
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
```

## Blueprints

```python
# blueprints/users.py
from flask import Blueprint

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
def list_users():
    return jsonify([])

# app.py
from blueprints.users import users_bp
app.register_blueprint(users_bp, url_prefix='/api')
```

## Jinja Templates

```html
{% extends "base.html" %}

{% block content %}
  <h1>{{ title }}</h1>
  {% for user in users %}
    <p>{{ user.name }}</p>
  {% endfor %}
{% endblock %}
```

## Common Extensions

| Extension | Purpose |
|-----------|---------|
| Flask-SQLAlchemy | Database ORM |
| Flask-Login | User auth |
| Flask-CORS | Cross-origin |
| Flask-Migrate | DB migrations |

## When to Apply
Use when building lightweight Python APIs or microservices.
