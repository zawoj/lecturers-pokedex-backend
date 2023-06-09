import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, storage
import json
import uuid
from colorthief import ColorThief

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16MB photos limit

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
bucket = storage.bucket("pokedex_photos")
db = firestore.client()
lecturers_ref = db.collection('lecturers')

def make_new_user(data, photo):
    if not 'name' in data:
            raise Exception("'name' is required")

    del data['_id']

    blob = bucket.blob(str(uuid.uuid1()) + '.jpeg')
    blob.upload_from_file(photo)

    data['image'] = blob.public_url

    color_thief = ColorThief(photo)
    dominant_color_rgb = color_thief.get_color(quality=1)
    dominant_color_hex = "#%2x%2x%2x" % dominant_color_rgb
    data["dominantColor"] = dominant_color_hex
    data["comments"] = []

    return data

@app.route('/users', methods=['POST'])
def create_user():
    print("Przyszedł POST")
    print(request.form)
    try:
        data = json.loads(request.form.get('data'))
        photo = request.files['file']
        user = make_new_user(data, photo)

        print(data)
        print(photo)

        lecturers_ref.add(user)
        print("kupa")
        return jsonify({"success": True}), 200
    except Exception as e:
        print("błomd ", e)
        return f"An Error Occurred: {e}"


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        data = json.loads(request.form.get('data'))
        photo = request.files['file']
        user = make_new_user(data, photo)

        lecturers_ref.document(id).set(user)
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
            all_lecturers.append({'_id' : doc.id, 'name':d['name'], 'image':d['image']})

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

@app.route('/users/<id>/comment', methods=['POST'])
def add_comment(id):
    try:
        json = request.get_json()
        if "comment" not in json:
            return "Comment was not provided", 500
        
        doc = lecturers_ref.document(id).get()
        lecturer = doc.to_dict()
        
        print(lecturer)

        if "comments" not in lecturer:
            lecturer["comments"] = []

        lecturer["comments"].append(json["comment"])

        print(lecturer)

        lecturers_ref.document(id).update(lecturer)

        return jsonify(lecturer), 200
    except Exception as e:
        return f"An Error Occurred: {e}"



port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)

