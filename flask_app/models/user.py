from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "users_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s,%(last_name)s,%(email)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, first_name = %(first_name)s, first_name = %(first_name)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def delete(cls, user_id):
        query = "DELETE FROM users WHERE id = %(id)s;"
        data = {"id" : user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First Name must be over 3 characters.")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last Name must be over 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!")
            is_valid = False
        return is_valid
