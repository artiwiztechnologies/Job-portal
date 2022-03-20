from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from werkzeug.utils import secure_filename
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
from flask import request, jsonify, send_file, send_from_directory, url_for, redirect, render_template
import os
import datetime

from models.company import CompanyModel
from models.products import ProductModel
from models.admin import AdminModel

UPLOAD_FOLDER = 'productPhotos'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

class newProduct(Resource):

    @jwt_required
    def post(self):

        DATA = dict(request.form)

        try:           
            if not (DATA['name'] and DATA['description'] and DATA['price'] and DATA['units']):
                return {'message': 'Values missing'}
        except:
            return {'message': 'Values missing'}

        jwt_id = get_jwt_identity()
        company = CompanyModel.find_by_id(jwt_id)

        if not company:
            return {'message': 'Not a company'}

        if not company.active:
            return {'message': 'Company not subscribed to an active plan.'}

        products_len = ProductModel.find_count_by_cid(jwt_id)
        if products_len >= 3:
            return {'message': 'Limit reached.'}

        if ProductModel.find_by_name_companyid(DATA['name'], jwt_id):
            return {'message': 'Product already exists'}

        data = dict()

        for KEY in DATA:
            if KEY != "photo":
                data[KEY] = DATA[KEY]

        data['photoURL'] = ""

        dateTime = str(datetime.datetime.now())
        DATE = dateTime[:10]
        date = datetime.datetime.strptime(DATE, "%Y-%m-%d").strftime("%d-%m-%Y")
        date = date.replace("-", "/")
        data['date'] = date

        data['company_id'] = jwt_id
        data['company_name'] = company.name

        product = ProductModel(**data)
        product.save_to_db()

        if 'photo' not in request.files:
            return {'message': 'Product added. No Photo uploaded!'}

        photos = request.files.getlist('photo')

        for photo in photos:
            if not (photo and '.' in photo.filename and photo.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
                return {'Message': 'Photo type not allowed'}

        try:

            for photo in photos:

                ext = secure_filename(photo.filename).rsplit('.', 1)[1].lower()
                URL = request.url_root[:-1]
                photoURL = "product-"+str(product.id)+"."+ext

                photo.save(os.path.join(UPLOAD_FOLDER, photoURL))

                product.photoURL = URL + "/product-picture/"+photoURL
                product.save_to_db()

                return {'message': 'Product added successfuly.', 'error': False}

        except:
            return{'message': "Failed to add product.", "error": True}


class Product(Resource):

    @jwt_required
    def get(self, id):
        try:
            product = ProductModel.find_by_id(id)
            if not product:
                return {'message': 'Product not found'}
            if product.enabled and product.admin_enabled:
                return {'product': product.json()}
            return {'message': 'Product disabled'}

        except: 
            return {'message': 'Error'}
    
    @jwt_required
    def delete(self, id):
        try:
            jwt_id = get_jwt_identity()
            jwt_id = get_jwt_identity()
            company = CompanyModel.find_by_id(jwt_id)

            if not company:
                return {'message': 'Not a company'}

            if not company.active:
                return {'message': 'Company not subscribed to an active plan.'}
            
            product = ProductModel.find_by_id_companyid(id, jwt_id)
            if not product:
                return {'message': 'Product not found'}
            product.delete_from_db()
            return {'message': 'Product deleted.'}
        except:
            return {'message': 'Error'}

    @jwt_required
    def put(self, id):

        jwt_id = get_jwt_identity()

        jwt_id = get_jwt_identity()
        company = CompanyModel.find_by_id(jwt_id)

        if not company:
            return {'message': 'Not a company'}

        if not company.active:
            return {'message': 'Company not subscribed to an active plan.'}

        product = ProductModel.find_by_id_companyid(id, jwt_id)
        if not product:
            return {'message': 'Product not found'}

        DATA = dict(request.form)

        try:           
            if not (DATA['name'] and DATA['description'] and DATA['price'] and DATA['units']):
                return {'message': 'Values missing'}
        except:
            return {'message': 'Values missing'}

        jwt_id = get_jwt_identity()
        company = CompanyModel.find_by_id(jwt_id)

        if not company:
            return {'message': 'Not a company'}

        data = dict()

        for KEY in DATA:
            if KEY != "photo":
                data[KEY] = DATA[KEY]

        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        product.units = data['units']
        product.save_to_db()

        dateTime = str(datetime.datetime.now())
        DATE = dateTime[:10]
        date = datetime.datetime.strptime(DATE, "%Y-%m-%d").strftime("%d-%m-%Y")
        date = date.replace("-", "/")

        product.date = date

        if 'photo' not in request.files:
            return {'message': 'Product updated.'}
        

        photos = request.files.getlist('photo')

        if photos and product.photoURL:
            File = product.photoURL.split('/')[-1]
            os.remove(UPLOAD_FOLDER+"/"+File)
            product.photoURL = ""

        product.save_to_db()

        for photo in photos:
            if not (photo and '.' in photo.filename and photo.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
                return {'message': 'Photo type not allowed'}

        try:

            for photo in photos:

                ext = secure_filename(photo.filename).rsplit('.', 1)[1].lower()
                URL = request.url_root[:-1]
                photoURL = "product-"+str(product.id)+"."+ext

                photo.save(os.path.join(UPLOAD_FOLDER, photoURL))

                product.photoURL = URL + "/product-picture/"+photoURL
                product.save_to_db()

                return {'message': 'Product updated successfuly.', 'error': False}

        except:
            return{'message': "Failed to update product.", "error": True}     


class ProductList(Resource):

    @jwt_required
    def get(self):
        try:
            # products = [product.json() for product in ProductModel.find_all()]
            jwt_id = get_jwt_identity()

            admin = AdminModel.find_by_id(jwt_id)
            
            if not admin or admin.status != 3:
                return {'message': 'Not an admin.'}
                
            products = []
            for product in ProductModel.find_all():
                if product.enabled and product.admin_enabled:
                    products.append(product.json())
            return {'lenght': len(products), 'products': products}, 200
        except:
            return {'message': 'Internal server error.'}, 500

class ProductPhoto(Resource):

    def get(self, path):
        try:
            return send_from_directory(UPLOAD_FOLDER, path=path, as_attachment=True)
        except FileNotFoundError:
            return {'message': 'File not Found'}, 404
        
class CompanyProductList(Resource):

    @jwt_required
    def get(self):
        try:
            cid = get_jwt_identity()
            products = [product.json() for product in ProductModel.find_all_by_companyid(cid)]
            return {'lenght': len(products), 'products': products}, 200
        except:
            return {'message': 'Internal server error.'}, 500

class ToggleProduct(Resource):

    @jwt_required
    def get(self, product_id):
        try:
            jwt_id = get_jwt_identity()
            
            if not CompanyModel.find_by_id(jwt_id):
                return {'message': 'Not a company.'}
            
            product = ProductModel.find_by_id_companyid(product_id, jwt_id)
            if not product:
                return {'message': 'Product not found.'}

            product.enabled = not product.enabled
            product.save_to_db()

            if product.enabled:
                return {'message': 'Enabled'}
            return {'message': 'Disabled'}
            
        except:
            return {'message': 'An error has occured!'}

class AdminToggle(Resource):

    @jwt_required
    def get(self, cid, product_id):
        try:
            jwt_id = get_jwt_identity()

            admin = AdminModel.find_by_id(jwt_id)
            
            if not admin or admin.status != 3:
                return {'message': 'Not an admin.'}
            
            product = ProductModel.find_by_id_companyid(product_id, cid)
            if not product:
                return {'message': 'Product not found.'}

            product.admin_enabled = not product.admin_enabled
            product.save_to_db()

            if product.admin_enabled:
                return {'message': 'Enabled'}
            return {'message': 'Disabled'}
            
        except:
            return {'message': 'An error has occured!'}

class ViewProductList(Resource):

    @jwt_required
    def get(self):
        try:
            companies = CompanyModel.find_all()
            arr = []
            for company in companies:
                # products = [product.json() for product in ProductModel.find_all_by_companyid(company.id)]
                products = []
                for product in ProductModel.find_all_by_companyid(company.id):
                    if product.enabled and product.admin_enabled:
                        products.append(product.json())
                if products:
                    arr.append({'name': company.name, 'products': products})
            return {'companies': arr}, 200
        except:
            return {'message': 'Internal server error.'}, 500