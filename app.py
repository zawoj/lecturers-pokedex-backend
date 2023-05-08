import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, storage
import json
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16MB photos limit

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
bucket = storage.bucket("pokedex_photos")
db = firestore.client()
lecturers_ref = db.collection('lecturers')

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = json.loads(request.form.get('data'))
        file = request.files['photo']

        if not 'name' in data:
            raise Exception("'name' is required")

        blob = bucket.blob(str(uuid.uuid1()) + '.jpeg')
        blob.upload_from_file(file)

        data['photo'] = blob.public_url

        lecturers_ref.add(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        data = json.loads(request.form.get('data'))
        file = request.files['photo']

        blob = bucket.blob(str(uuid.uuid1()) + '.jpeg')
        blob.upload_from_file(file)

        data['photo'] = blob.public_url

        lecturers_ref.document(id).set(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        lecturers_ref.document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/users', methods=['GET'])
def read_all_users():
    try:
        all_lecturers = []
        for doc in lecturers_ref.stream():
            d = doc.to_dict()
            d['_id'] = doc.id
            all_lecturers.append({'_id' : doc.id, 'name':d['name']})

        return jsonify(all_lecturers), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/users/<id>', methods=['GET'])
def read_user(id):
    try:
        doc = lecturers_ref.document(id).get()
        d = doc.to_dict()
        d['_id'] = doc.id

        return jsonify(d), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)

