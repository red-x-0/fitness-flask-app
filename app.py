from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.fitnessDB
exercises = db.exercises

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    purpose = request.form['purpose']
    weight = int(request.form['weight'])
    height = int(request.form['height'])
    age = int(request.form['age'])
    location = request.form['location']

    query = {
        'type': purpose,
        'minWeight': {'$lte': weight},
        'maxWeight': {'$gte': weight},
        'minHeight': {'$lte': height},
        'maxHeight': {'$gte': height},
        'minAge': {'$lte': age},
        'maxAge': {'$gte': age},
        'location': location
    }

    results = list(exercises.find(query, {'_id': 0}))
    return render_template('results.html', exercises=results)

if __name__ == '__main__':
    app.run(debug=True)

