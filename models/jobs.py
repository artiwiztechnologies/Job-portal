# from db import db
# import datetime
# import requests

# class JobsModel(db.Model):
#     __tablename__ = "jobs"

#     id = db.Column(db.Integer, primary_key=True)
#     company_id = db.Column(db.Integer)
#     title = db.Column(db.String(80))
#     description = db.Column(db.String(500))
#     applicants = db.Column(db.String())
#     available = db.Column(db.Boolean())

#     def __init__(self, company_id, title, description, applicants, available):
#         self.company_id = company_id
#         self.title = title
#         self.description = description
#         self.applicants = applicants
#         self.available = available

#     def json(self):
#         return {
#             "title": self.title,
#             "company_id": self.company_id,
#             "description": self.description,
#             "applicants": self.applicants,
#             "available": self.available
#         }

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()

#     @classmethod
#     def find_by_title(cls, title):
#         return cls.query.filter_by(title=title).first()

#     @classmethod
#     def find_by_id(cls, _id):
#         return cls.query.filter_by(id=_id).first()