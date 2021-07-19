from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_user
import re

DATABASE_SCHEMA = 'python_exam_2_db'

class Band:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.home_city = data['home_city']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def get_creator(self):
        return model_user.User.get_one(self.creator_id)


# C !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def create(cls, info):
        query = 'INSERT INTO bands (name, genre, home_city, creator_id) VALUES (%(name)s, %(genre)s, %(home_city)s, %(creator_id)s)'
        data = {
            'name' : info['name'],
            'genre' : info['genre'],
            'home_city' : info['home_city'],
            'creator_id' : info['creator_id'],
        }

        new_bands_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

        return new_bands_id

    @classmethod
    def join_one(cls, info):
        query = 'INSERT INTO members (user_id, band_id) VALUES (%(user_id)s, %(band_id)s) '
        data = {
            'user_id': info['user_id'],
            'band_id': info['band_id'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
    
# R !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM bands;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if len(results) > 0:
            all_bands = []
            for bands in results:
                all_bands.append(cls(bands))
            return all_bands
        return results

    @classmethod
    def get_one(cls, name_id):
        query = 'SELECT * FROM bands WHERE id = %(name_id)s;'
        data = {
            'name_id': name_id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        one_bands = []
        if len(results) > 0:
           return cls(results[0])
        return results
    
# U !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def update_one(cls, info):
        query = 'UPDATE bands SET name=%(name)s, genre=%(genre)s, home_city=%(home_city)s WHERE id=%(band_id)s'
        data = {
            'name': info['name'],
            'genre': info['genre'],
            'home_city': info['home_city'],
            'band_id': info['band_id'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)



# D !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def delete_one(cls, band_id):
        query = 'DELETE FROM bands WHERE id=%(band_id)s'
        data = {
            'band_id': band_id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return id

    @classmethod
    def leave_one(cls, info):
        query = 'DELETE FROM members WHERE user_id=%(user_id)s AND band_id = %(band_id)s'
        data = {
            'user_id': info['user_id'],
            "band_id": info['band_id']
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return id


# ******************************************* VALIDATIONS ********************************************
    @staticmethod
    def validate_bands(user_data):
        is_valid = True

        if len(user_data['name']) < 3: 
            is_valid = False
            flash('name name must be greater than 3 characters')

        if len(user_data['genre']) < 3: 
            is_valid = False
            flash('Genre must be greater than 3 characters')

        if len(user_data['home_city']) < 3: 
            is_valid = False
            flash('Home City must be greater than 3 characters')
        
        return is_valid