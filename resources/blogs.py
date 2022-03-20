from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from werkzeug.utils import secure_filename
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
from flask import request, jsonify, send_file, send_from_directory, url_for, redirect, render_template
import os
import datetime

from models.admin import AdminModel
from models.blogs import BlogModel
from models.blogComments import BlogCommentsModel
from models.helper import Helper

UPLOAD_FOLDER = 'blogPhotos'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

class newBlog(Resource):

    @jwt_required
    def post(self):

        jwt_id = get_jwt_identity()
        admin = AdminModel.find_by_id(jwt_id)

        if not admin or admin.status != 3:
            return {'message': 'Not an admin.'}
        
        DATA = dict(request.form)

        try:           
            if not (DATA['title'] and DATA['content']):
                return {'message': 'Values missing'}
            
        except:
            return {'message': 'Values missing'}
        
        data = dict()

        for KEY in DATA:
            if KEY != "photo":
                data[KEY] = DATA[KEY]

        data['photoURL'] = ""

        dateTime = str(datetime.datetime.now())
        DATE = dateTime[:10]
        date = datetime.datetime.strptime(DATE, "%Y-%m-%d").strftime("%d-%m-%Y")
        date = date.replace("-", "/")
        # print(date)
        data['date'] = date


        blog = BlogModel(**data)
        blog.save_to_db()

        if 'photo' not in request.files:
            return {'message': 'Blog added. No Photo uploaded!'}

        photos = request.files.getlist('photo')

        for photo in photos:
            if not (photo and '.' in photo.filename and photo.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
                return {'Message': 'Photo type not allowed'}

        try:

            for photo in photos:

                ext = secure_filename(photo.filename).rsplit('.', 1)[1].lower()
                URL = request.url_root[:-1]
                photoURL = "blog-"+str(blog.id)+"."+ext

                photo.save(os.path.join(UPLOAD_FOLDER, photoURL))

                blog.photoURL = URL + "/blog-picture/"+photoURL
                blog.save_to_db()

                return {'message': 'Blog added successfuly.', 'error': False}

        except:
            return{'message': "Failed to add blog.", "error": True}

class Blog(Resource):

    @jwt_required
    def get(self, id):
        try:
            blog = BlogModel.find_by_id(id)

            if not blog:
                return {'message': "Blog not found"}

            comment = [comment.json() for comment in BlogCommentsModel.find_by_blog_id(blog.id)]
            
            return {'blog': blog.json(), 'comments': comment}

        except:
            return {'message': 'Error'}


    @jwt_required
    def delete(self, id):
        try:
            jwt_id = get_jwt_identity()
            admin = AdminModel.find_by_id(jwt_id)

            if not admin or admin.status != 3:
                return {'message': 'Not an admin.'}

            blog = BlogModel.find_by_id(id)

            if not blog:
                return {'message': "Blog not found"}

            Helper.del_blog_comments_by_blog(blog.id)

            blog.delete_from_db()
            
            return {'message': 'Blog deleted'}

        except:
            return {'message': 'Error'}

    @jwt_required
    def put(self, id):

        jwt_id = get_jwt_identity()
        admin = AdminModel.find_by_id(jwt_id)

        if not admin or admin.status != 3:
            return {'message': 'Not an admin.'}

        blog = BlogModel.find_by_id(id)

        if not blog:
            return {'message': "Blog not found"}
        
        DATA = dict(request.form)

        try:           
            if not (DATA['title'] and DATA['content']):
                return {'message': 'Values missing'}
            
        except:
            return {'message': 'Values missing'}
        
        data = dict()

        for KEY in DATA:
            if KEY != "photo":
                data[KEY] = DATA[KEY]

        blog.title = data['title']
        blog.content = data['content']
        blog.date = data['date']
        blog.links = data['links']
        blog.save_to_db()


        dateTime = str(datetime.datetime.now())
        DATE = dateTime[:10]
        date = datetime.datetime.strptime(DATE, "%Y-%m-%d").strftime("%d-%m-%Y")
        date = date.replace("-", "/")

        blog.date = date

        if 'photo' not in request.files:
            return {'message': 'Blog updated.'}

        photos = request.files.getlist('photo')

        if photos and blog.photoURL:
            File = blog.photoURL.split('/')[-1]
            os.remove(UPLOAD_FOLDER+"/"+File)
            blog.photoURL = ""
        
        blog.save_to_db()

        for photo in photos:
            if not (photo and '.' in photo.filename and photo.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
                return {'message': 'Photo type not allowed'}

        try:

            for photo in photos:

                ext = secure_filename(photo.filename).rsplit('.', 1)[1].lower()
                URL = request.url_root[:-1]
                photoURL = "blog-"+str(blog.id)+"."+ext

                photo.save(os.path.join(UPLOAD_FOLDER, photoURL))

                blog.photoURL = URL + "/blog-picture/"+photoURL
                blog.save_to_db()

                return {'message': 'Blog updated successfuly.', 'error': False}

        except:
            return{'message': "Failed to update blog.", "error": True}



class BlogPhoto(Resource):

    def get(self, path):
        try:
            return send_from_directory(UPLOAD_FOLDER, path=path, as_attachment=True)
        except FileNotFoundError:
            return {'message': 'File not Found'}, 404

class AllBlogs(Resource):

    @jwt_required
    def get(self):
        try:
            blogs = [blog.json() for blog in BlogModel.find_all()]
            return {'blogs': blogs}
        except:
            return {'message': 'Error'}