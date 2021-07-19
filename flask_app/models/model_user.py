from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_bands
import re

DATABASE_SCHEMA = 'python_exam_2_db'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.hash_pw = data['hash_pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def in_band(self, band_id):
        query = 'SELECT * FROM members WHERE members.band_id = %(band_id)s AND user_id = %(user_id)s'
        data = {
            "user_id": self.id,
            "band_id": band_id
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print(result)
        if len(result):
            return True
        return False

    def get_bands(self):
        query = 'SELECT * FROM bands WHERE creator_id = %(creator_id)s'
        data = {
            "creator_id": self.id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results):
            all_bands = []
            for band in results: 
                temp_band = model_bands.Band.get_one(band['id'])   
                all_bands.append(temp_band)
            return all_bands
        return results

    def get_joined_bands(self):
        query = 'SELECT * FROM members JOIN bands ON band_id = bands.id WHERE user_id = %(user_id)s;'
        data = {
            "user_id": self.id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results):
            all_bands = []
            for band in results:
                temp_band = model_bands.Band.get_one(band['id'])   
                all_bands.append(temp_band)
            return all_bands
        return results

    @property
    def full_name(self):
        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

    def __repr__(self) -> str:
        display = f'id: {self.id},  first name: {self.first_name}, last name: {self.last_name}, email: {self.email}, hash_pw: {self.hash_pw}, created_at: {self.created_at}, updated_at: {self.updated_at}'
        return display

# C
    @classmethod
    def create(cls, info):
        query = 'INSERT INTO users (first_name, last_name, email, hash_pw) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(hash_pw)s)'
        data = {
            'first_name': info['first_name'],
            'last_name': info['last_name'],
            'email': info['email'],
            'hash_pw': info['hash_pw'],
        }
        new_user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_user_id
    
# R
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)

        all_users = []
        for user in results:
            all_users.append(cls(user))

        return all_users

    @classmethod
    def get_one(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        data ={
            'id': id
        }
        return cls(connectToMySQL(DATABASE_SCHEMA).query_db(query,data)[0])

    
    @classmethod
    def get_one_by_email(cls, email):
        query= 'SELECT * FROM users WHERE email = %(email)s;'
        data = {
            'email' : email
        }

        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data) # returns a list of dictionaries ( in this case only one dictionary)

        return result
    

# U
    @classmethod
    def update_one(cls, info):
        # TODO: add the ability to update pw 
        query = 'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, hash_pw=%(hash_pw)s WHERE id=%(id)s'
        data = {
            'first_name': info['first_name'],
            'last_name': info['last_name'],
            'email': info['email'],
            'hash_pw': info['hash_pw'],
            'id': info['id'],
        }

        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# D
    @classmethod
    def delete_one(cls, id):
        query = 'DELETE FROM users WHERE id=%(id)s'
        data = {
            'id': id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        print(f'user with the id {id} has been deleted')
        return id

    @staticmethod
    def validate_user(form_data):
        is_valid = True
        
        if len(form_data['first_name']) < 3:
            flash('First name must be greater than 3 characters. ')
            is_valid = False
        
        if len(form_data['last_name']) < 3:
            flash('Last name must be greater than 3 characters. ')
            is_valid = False

        if len(form_data['email']) < 3:
            flash('Email must be greater than 3 characters. ')
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(form_data['email']):
            flash('Invalid email address')
            is_valid = False

        user = User.get_one_by_email(form_data['email'])
        if len(user) >= 1:
            flash('username is already taken')

        if len(form_data['pw']) < 8:
            flash('Password must be greater than 8 characters. ')
            is_valid = False

        if form_data['pw'] != form_data['confirm_pw']:
            flash('Passwords do not match')
            is_valid = False
        
        return is_valid