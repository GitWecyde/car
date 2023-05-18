import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request, jsonify
from pyasn1.compat.octets import null

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

#create users
@app.route('/users', methods=['POST'])
def users():
    data = request.json
    email = request.json.get('email')
    name = request.json.get('name')
    firstname = request.json.get('firstname')
    pseudo = request.json.get('pseudo')
    age = request.json.get('age')
    if email and name and firstname and pseudo and age:
        db.collection("users").document(email).set(data)
        return jsonify({"message": "User created successfully", "user": data}), 201
    else:
        return jsonify({"error": "problème avec les données"}), 400


#delete users
@app.route('/delete/users/<email>', methods=['GET'])
def delete_users(email):
    deleteUsers = db.collection('users').document(email).delete()

    return {"status": "success",}, 200

#update users
@app.route('/update/users', methods=['PUT'])
def update_user():
    data = request.json
    email = request.json.get('email')
    name = request.json.get('name')
    firstname = request.json.get('firstname')
    pseudo = request.json.get('pseudo')
    age = request.json.get('age')
    if email and name and firstname and pseudo and age:
        user_ref = firestore.client().collection('users').document(email)
        user = user_ref.get()
        if user.exists:
            user_ref.update({
                'name': name,
                'firstname': firstname,
                'pseudo': pseudo,
                'age': age
            })
            return jsonify({"message": "User updated successfully", "user": data}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Email or name missing"}), 400

'''
CRUD de la voiture 
'''
#create cars
@app.route('/cars', methods=['POST'])
def cars():
    data = request.json
    marque = request.json.get('marque')
    kilometrage = request.json.get('kilometrage')
    nom_voiture = request.json.get('nom_voiture')
    prix = request.json.get('prix')
    boite_de_vitesse = request.json.get('boite_de_vitesse')
    type_carburant = request.json.get('type_carburant')

    missing_fields = []
    for field, value in data.items():
        if not value:
            missing_fields.append(field)

    if missing_fields:
        return jsonify({"error": f"Les champs suivants sont manquants ou nuls : {', '.join(missing_fields)}"}), 400

    if marque and kilometrage and nom_voiture and prix and boite_de_vitesse and type_carburant:
        db.collection("cars").document(marque).set(data)
        return jsonify({"message": "Car created successfully", "car": data}), 201
    else:
        return jsonify({"error": "problème avec les données"}), 400


@app.route('/read/cars', methods=['GET'])
def get_cars():
    conv_ref = db.collection("cars")
    docs = conv_ref.stream()

    conversations = []
    for doc in docs:
        conversations.append(doc.to_dict())

    return {"status": "success", "data": conversations}, 200

@app.route('/update/cars', methods=['PUT'])
def update_cars():
    data = request.json
    marque = request.json.get('marque')
    kilometrage = request.json.get('kilometrage')
    nom_voiture = request.json.get('nom_voiture')
    prix = request.json.get('prix')
    boite_de_vitesse = request.json.get('boite_de_vitesse')
    type_carburant = request.json.get('type_carburant')
    if marque and kilometrage and nom_voiture and prix and boite_de_vitesse and type_carburant:
        user_ref = firestore.client().collection('cars').document(marque)
        user = user_ref.get()
        if user.exists:
            user_ref.update({
                'marque': marque,
                'kilometrage': kilometrage,
                'nom_voiture': nom_voiture,
                'prix': prix,
                "boite_de_vitesse": boite_de_vitesse,
                "type_carburant":type_carburant
            })
            return jsonify({"message": "Car updated successfully", "car": data}), 200
        else:
            return jsonify({"error": "car not found"}), 404
    else:
        return jsonify({"error": "marque or name missing"}), 400


@app.route('/delete/cars/<marque>', methods=['GET'])
def delete_cars(marque):
    deleteCars = db.collection('cars').document(marque).delete()

    return {"status": "success"}, 200
'''
CRUD du chat
'''
@app.route('/chats', methods=['POST'])
def chat():
    data = request.get_json()

    email = data.get("email")
    name = data.get("name")
    message = data.get("message")
    date = data.get("date")

    doc_ref = db.collection("chats").document(email).collection("conversation").document(date)

    chat_data = {
        "name": name,
        "date" : date,
        "message": message
    }

    doc_ref.set(chat_data)

    return {"status": "success", "data": chat_data}, 200


@app.route('/chats/conv/<email>', methods=['GET'])
def get_conversations(email):
    conv_ref = db.collection("chats").document(email).collection("conversation")
    docs = conv_ref.stream()

    conversations = []
    for doc in docs:
        conversations.append(doc.to_dict())

    return {"status": "success", "data": conversations}, 200


'''
CRUD actualité
'''


@app.route('/actu', methods=['POST'])
def actu():
    data = request.get_json()
    message = data.get("message")
    titre = data.get("titre")

    doc_ref = db.collection("actualité").document(titre)

    chat_data = {
        "titre": titre,
        "message": message
    }

    doc_ref.set(chat_data)

    return {"status": "success", "data": chat_data}, 200


@app.route('/actu/read', methods=['GET'])
def recupactu():
    conv_ref = db.collection("actualité")
    docs = conv_ref.stream()

    conversations = []
    for doc in docs:
        conversations.append(doc.to_dict())

    return {"status": "success", "data": conversations}, 200

@app.route('/actu/delete/<titre>', methods=['GET'])
def delete_actu(titre):
    deleteCars = db.collection('actualité').document(titre).delete()

    return {"status": "success"}, 200

'''
CRUD Location
'''


@app.route('/location', methods=['POST'])
def create_location():
    data = request.get_json()
    email = data.get("email")
    marque = data.get("marque")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    prix = data.get("prix")
    status = data.get("status")
    payment = data.get("payment")

    doc_ref = db.collection("location").document(email)

    chat_data = {
        "email": email,
        "marque": marque,
        "start_date": start_date,
        "end_date": end_date,
        "prix": prix,
        "status": status,
        "payment": payment
    }

    doc_ref.set(chat_data)

    return {"status": "success", "data": chat_data}, 200


@app.route('/location/read', methods=['GET'])
def recup_location():
    conv_ref = db.collection("location")
    docs = conv_ref.stream()

    conversations = []
    for doc in docs:
        conversations.append(doc.to_dict())

    return {"status": "success", "data": conversations}, 200


@app.route('/location/update', methods=['PUT'])
def update_location():
    data = request.get_json()
    email = data.get("email")
    marque = data.get("marque")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    prix = data.get("prix")
    status = data.get("status")
    payment = data.get("payment")
    if email and marque and start_date and end_date and prix and status and payment:
        user_ref = firestore.client().collection('location').document(email)
        user = user_ref.get()
        if user.exists:
            user_ref.update({
                "email": email,
                "marque": marque,
                "start_date": start_date,
                "end_date": end_date,
                "prix": prix,
                "status": status,
                "payment": payment
            })
            return jsonify({"message": "location updated successfully", "car": data}), 200
        else:
            return jsonify({"error": "location not found"}), 404
    else:
        return jsonify({"error": "location or name missing"}), 400


@app.route('/location/delete/<email>', methods=['GET'])
def delete_location(email):
    delete_location = db.collection('location').document(email).delete()

    return {"status": "success"}, 200

if __name__ == '__main__':
    app.run(debug=True)

# création de la collection et envoi de données
"""
data = {
    "lastname": "iloki",
    "first name": "ipourou-idihi",
    "age ": 25
}
db.collection('persons').add(data)

"""

# creation de la collection avec un id défini
"""
data = {
    "nom": "2008",
    "km": "200000",
    "location ": True
}
db.collection("cars").document("peugeot").set(data)

"""

# ajouter des données à un document ayant une données existantes
# db.collection("cars").document("peugeot").set({"price per day" : 100}, merge= True)

# créer une sous collection dans une collection
"""
data = {
    "psychologie" : "le language corporel"
}
db.collection("persons").document("ipourou").collection("books").add(data)

"""
# créer une sous collection avec un id spécifique et une donnée spécifique
"""
data = {
    "sarah" : "en date"
}
db.collection("persons").document("ipourou").collection("habits").document("girls").set({"sarah" : "ken"})
"""

# modifier la donées d"une collection ou sous collection
# db.collection("nom de la collection").document("id du document").set({"nom de la donnée à modifier ou ajouter " : "valeur de la données à modifier ou ajouter"})

# Read data quand on connait l'id du document
"""
result = db.collection("persons").document("ipourou").collection("habits").document("girls").get()
if (result.exists):
    print(result.to_dict())

"""

# récupère tous les documents dans une collection
"""
result  = db.collection("persons").get()
for doc in result:
    print(doc.to_dict())
"""

# querying equals (se renseigner pour faire les requetes python)

# updatedata- know key

"""
data = {
    "chmap": "update"
}
db.collection("persons").document("ipourou").update(data)

"""
# db.collection("persons").document("ok7VzXEKdud9in3253zx").update({"age":firestore.Increment(10)})

"""docs = db.collection("persons").get()
for doc in docs:
    print(doc.to_dict()["age"])"""

"""
envoyé les infos utilisateurs avec l'id qui est le nom de l'utilisateur
db.collection("users").document(data['name']).set(data)
"""

"""
envoyé les infos de la voiture de l'admin vers la base de données
db.collection("cars").document(data["marque"]).set(data)
"""

"""
envoyé les données de location
db.collection("Location").document(data["email"]).set(data)
"""
