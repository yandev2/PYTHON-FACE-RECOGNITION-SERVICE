import os
from flask import request, jsonify
from functools import wraps

def secure_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key and api_key == os.getenv('API_KEY'):
            return f(*args, **kwargs)
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    return decorated_function

def clear_temp_file(path):
    if os.path.exists(path):
        os.remove(path)