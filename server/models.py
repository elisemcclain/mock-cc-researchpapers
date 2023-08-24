from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Research(db.Model, SerializerMixin):
    __tablename__ = 'researchs'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    research_authors = db.relationship('ResearchAuthors', cascade='all, delete', backref='research')

    serialize_rules = ('-research_authors.research', '-created_at', '-updated_at',)

    # TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
    authors = association_proxy('research_authors', 'author')

    @validates('year')
    def validate_year(self, key, year):
        if not 1000 <= year <= 9999:
            raise ValueError('please give a valid year')
        return year
        


class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_authors = db.relationship('ResearchAuthors', cascade='all, delete', backref='author')

    serialize_rules = ('-research_authors.author', '-created_at', '-updated_at',)

    # TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
    serialize_only = ('id', 'name', 'field_of_study',)


    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        allowed_fields = ['AI', 'Robotics', 'Machine Learning', 'Vision', 'Cybersecurity']
        if field_of_study not in allowed_fields:
            raise ValueError('please give a valid study')
        return field_of_study



class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('researchs.id'))

    serialize_rules = ('-author.research_authors', '-research.research_authors', '-created_at', '-updated_at',)

    # TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
    # serialize_only = ('id', 'name', 'field_of_study',)