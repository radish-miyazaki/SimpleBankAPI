from flask import Flask
from pymongo import MongoClient

from handlers import bp

app = Flask(__name__)
app.register_blueprint(bp)

# Setup MongoDB
client = MongoClient('mongodb://db:27017')
db = client["BankAPI"]
users = db["Users"]

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
