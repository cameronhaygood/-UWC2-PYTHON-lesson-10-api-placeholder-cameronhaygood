from pathlib import Path

from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, instance_path=str(Path(".").absolute()))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///social_network.db"

db = SQLAlchemy(app)
api = Api(app)

class UserRecord(db.Model):

    __tablename__ = 'usertable'
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

class User(Resource):
    def get(self):
        return jsonify([record.serialize() for record in UserRecord.query.all()])


#Define End Points
api.add_resource(User, "/users")

if __name__ == '__main__':
    app.run(port=5002, debug=True)