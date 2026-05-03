import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from core.logic import extract_face_features, verify_face_features
from utils.helpers import secure_api, clear_temp_file

load_dotenv()
app = Flask(__name__)
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/api/extract', methods=['POST'])
@secure_api # Dekorator untuk cek API Key
def extract():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image uploaded"}), 400
    
    file = request.files['image']
    temp_path = f"uploads/reg_{file.filename}"
    file.save(temp_path)
    
    try:
        embedding = extract_face_features(temp_path)
        return jsonify({"status": "success", "embedding": embedding})
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 422
    finally:
        clear_temp_file(temp_path)

@app.route('/api/verify', methods=['POST'])
@secure_api
def verify():
    if 'image' not in request.files or 'registered_embedding' not in request.form:
        return jsonify({"status": "error", "message": "Data incomplete"}), 400

    file = request.files['image']
    reg_embedding = request.form['registered_embedding']
    temp_path = f"uploads/ver_{file.filename}"
    file.save(temp_path)

    try:
        result = verify_face_features(temp_path, reg_embedding)
        return jsonify({"status": "success", **result})
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
    finally:
        clear_temp_file(temp_path)

if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    debug = os.getenv('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)