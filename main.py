from flask import Flask, request, jsonify

import urllib
import pyrebase


#fichier de configuration de mon compte firebase
firebaseConfig = {
    "apiKey": "AIzaSyDkaSEVy5dWWSQ-BIFlXIkK9eX-wVayezA",
    "authDomain": "mtleasecar-6062f.firebaseapp.com",
    "databaseURL": "https://mtleasecar-6062f-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "mtleasecar-6062f",
    "storageBucket": "mtleasecar-6062f.appspot.com",
    "messagingSenderId": "689507401845",
    "appId": "1:689507401845:web:8d5ed8e39c145d1f43b83c"
}

firebase = pyrebase.initialize_app(firebaseConfig) #initialisation du projet

db = firebase.database()

auth = firebase.auth()

storage = firebase.storage()

app= Flask(__name__)

@app.route('/users',methods=['POST'])
def users():
    data = request.json
    name = data.get('name')
    db.collection("users").document(name).set(data)


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    auth.sign_in_with_email_and_password(email, password)

@app.route('/signup', methods=['POST'])
def SignUp():
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        user = auth.create_user_with_email_and_password(email,password)
        return jsonify({"message": "success"})
    except:
        return jsonify({
            "message": "ile mail existe déjà"
        })

@app.route('/storagefile', methods=['POST'])
def storagefile():
    cloudfilename = request.form.get('cloudfilename') #le nom du fichier dans le dossier
    filename = request.form.get('filename') #le nom qu'il aura dans la database
    try:
        storage.child(cloudfilename).put(filename)
        return jsonify({"message": "success"})
    except:
        return jsonify({
            "message": "quelque chose ne va pas ..."
        })


@app.route('/fileread', methods=['POST'])
def fileread():
    cloudfilename = request.form.get('cloudfilename')
    url = storage.child(cloudfilename).get_url(None)
    try:
        urllib.request.urlopen(url).read()
        return jsonify({"message": "success"})
    except:
        return jsonify({"message": "problème survenu"})


#database
@app.route('/insertdataUsers', methods=['POST'])
def insertdataUsers():
    data = request.form.get('data')
    uid = request.form.get('uid')
    try:
        db.child("users").child(uid).set(data) #permet de créer un dossier qui va contenir les données envoyés en paramètres
        return jsonify({"message": "success"})
    except:
        return jsonify({"message": "problème survenu"})

#update
@app.route('/updatedata', methods=['POST'])
def updatedata():
    collection = request.form.get('collection')
    champs = request.form.get('champs')
    key = request.form.get('key')
    value = request.form.get('value')
    try:
        db.child(collection).child(champs).update({key: value})
        return jsonify({"message": "success"})
    except:
        return jsonify({"message": "problème survenu"})


#delete
@app.route('/deleteUsers', methods=['POST'])
def deleteUsers():
    uid = request.form.get('uid')
    try:
        db.child("users").child(uid).remove()
        return jsonify({"message": "success"})
    except:
        return jsonify({"message": "problème survenu"})


#read
@app.route('/readData', methods=['POST'])
def readData(collection):
    collection = request.form.get('collection')
    db.child(collection).get()

if __name__ == '__main__':
    app.run(debug=True)