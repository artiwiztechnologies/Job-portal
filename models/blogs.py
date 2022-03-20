from db import db
import datetime
import requests

from models.admin import AdminModel

class BlogModel(db.Model):

    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    links = db.Column(db.String())
    photoURL = db.Column(db.String())
    docs = db.Column(db.String())
    enabled = db.Column(db.Boolean(), default=True)
    date = db.Column(db.String(), default="")

    def __init__(self, title, content, links, photoURL, date):

        self.title = title
        self.content = content
        self.links = links
        self.photoURL = photoURL
        self.date = date

    def json(self):
        
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "links": self.links.split(','),
            "photoURL": self.photoURL,
            "date": self.date
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()