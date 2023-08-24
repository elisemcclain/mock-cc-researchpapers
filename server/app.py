#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# is it ok that my research class is the same in models AND app?
class ResearchRes(Resource):
    def get(self):
        research = [r.to_dict(rules=('-research_authors', '-created_at', '-updated_at',)) for r in Research.query.all()]
        return make_response(research, 200)

api.add_resource(ResearchRes, '/research')

class ResearchById(Resource):
    def get(self, id):
        research = Research.query.filter(Research.id == id).first()

        if not research:
            return make_response({"error": "Research paper not found"}, 404)
        
        return make_response(research.to_dict(rules=('-created_at', '-updated_at',)), 200)

    def delete(self, id):
        research = Research.query.filter(Research.id == id).first()

        if not research:
            return make_response({"error": "Research paper not found"}, 404)

        if research:
            db.session.delete(research)
            db.session.commit()
        return make_response({}, 204)


api.add_resource(ResearchById, '/research/<int:id>')

class Authors(Resource):
    def get(self):
        author = [a.to_dict(rules=('-research_authors', '-created_at', '-updated_at',)) for a in Author.query.all()]
        return make_response(author, 200)

api.add_resource(Authors, '/authors')

class ResearchAuthorsR(Resource):
    def post(self):
        new_research_author = ResearchAuthors()
        data = request.get_json()

        try:
            for key in data:
                setattr(new_research_author, key, data[key])
            
            db.session.add(new_research_author)
            db.session.commit()
            return make_response(new_research_author.author.to_dict(), 201)
        
        except ValueError as error:
            new_error = {"errors": str(error)}
            return make_response(new_error, 400)

api.add_resource(ResearchAuthorsR, '/research_authors')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
