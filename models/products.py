from db import db
import datetime
import requests

from models.company import CompanyModel

# - name
# - photo
# - id
# - description
# - companyid(company details included)
# - price (not decided)

class ProductModel(db.Model):

    __tablename__ = "company-products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    company_id = db.Column(db.Integer)
    company_name = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.String())
    photoURL = db.Column(db.String())
    units = db.Column(db.Integer)
    enabled = db.Column(db.Boolean(), default=True)
    admin_enabled = db.Column(db.Boolean(), default=True)
    date = db.Column(db.String())
    time = db.Column(db.String())

    def __init__(self, name, company_id, company_name, description, price, photoURL, units, date):
        self.name = name
        self.company_id = company_id
        self.company_name = company_name
        self.description = description
        self.price = price
        self.photoURL = photoURL
        self.units = units
        self.date = date

    def json(self):

        company = CompanyModel.find_by_id(self.company_id)
        
        if not company:
            return {'message': 'Company not found!'}

        return{
            "id": self.id,
            "name": self.name,
            "company_id": self.company_id,
            "company_name": self.company_name,
            "company_phonenumber": company.phonenumber,
            "company_email": company.email,
            "company_photo": company.photoURL,
            "photoURL": self.photoURL,
            "description": self.description,
            "units": self.units,
            "price": self.price,
            "enabled": self.enabled,
            "admin_enabled": self.admin_enabled,
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
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_name_companyid(cls, name, cid):
        return cls.query.filter_by(name=name, company_id=cid).first()

    @classmethod
    def find_all_by_companyid(cls, cid):
        return cls.query.filter_by(company_id=cid)

    @classmethod
    def find_by_companyid(cls, cid):
        return cls.query.filter_by(company_id=cid).first()

    @classmethod
    def find_by_id_companyid(cls, id, cid):
        return cls.query.filter_by(id=id, company_id=cid).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_count_by_cid(cls, id):
        return cls.query.filter_by(company_id = id).count()

