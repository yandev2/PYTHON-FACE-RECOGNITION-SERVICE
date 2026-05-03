import json
from deepface import DeepFace
from scipy.spatial import distance

MODEL_NAME = "Facenet512"

def extract_face_features(img_path):
    objs = DeepFace.represent(
        max_faces=1,
        img_path=img_path,
        model_name=MODEL_NAME,
        enforce_detection=True,
        detector_backend='retinaface',
        align=True)
    return objs[0]["embedding"]

def verify_face_features(img_path, registered_embedding_str):
    # Dapatkan embedding foto baru
    new_objs = DeepFace.represent(
        max_faces=1,
        img_path=img_path,
        model_name=MODEL_NAME,
        detector_backend='retinaface',
        align=True)
    face_data = new_objs[0]
    new_embedding = face_data["embedding"]
    
    # Parse embedding lama
    reg_embedding = json.loads(registered_embedding_str)
    
    # Hitung similarity
    dist = distance.cosine(reg_embedding, new_embedding)
    threshold = 0.4
    is_match = dist < threshold
    
    return {
        "match": bool(is_match),
        "is_real": True,
        "score": round((1 - dist) * 100, 2),
        "distance": round(float(dist), 4),
        "message": "Wajah asli terverifikasi" if is_match else "Wajah tidak cocok"
    }