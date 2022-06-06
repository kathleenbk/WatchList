from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Watchlist:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']

    @classmethod
    def save_watchlist(cls, data):
        query = "INSERT INTO watchlists (name, user_id) VALUES ( %(name)s, %(user_id)s );"
        return connectToMySQL('movies_schema').query_db( query, data )

    @classmethod
    def get_all_watchlists(cls):
        query = "SELECT * FROM watchlists;"
        results = connectToMySQL('movies_schema').query_db(query)
        watchlists = []
        for watchlist in results:
            watchlists.append(cls(watchlist))
        return watchlists
    
    @classmethod
    def get_user_watchlists(cls, data):
        query = "SELECT * FROM watchlists LEFT JOIN users ON watchlists.user_id = users.id;"
        results = connectToMySQL('movies_schema').query_db(query, data)
        watchlists = []
        if results:
            
            for row_from_db in results:
                user_data = {
                    "id": row_from_db["users.id"],
                    "first_name": row_from_db["first_name"],
                    "last_name": row_from_db["last_name"],
                    "email": row_from_db["email"],
                    "password": row_from_db["password"],
                    "created_at": row_from_db["users.created_at"],
                    "updated_at": row_from_db["users.updated_at"]
                }
                watchlist=cls(row_from_db)
                owner=user.User(user_data)
                watchlist.owner = owner

                watchlists.append(watchlist)
        return watchlists

    @classmethod
    def get_one_watchlist(cls, data):
        query = "SELECT * FROM watchlists LEFT JOIN users ON watchlists.user_id = users.id WHERE watchlists.id = %(id)s;"
        result = connectToMySQL('movies_schema').query_db(query,data)
        if result:
            watchlist=cls(result[0])
            user_data = {
                "id": result[0]["users.id"],
                "first_name": result[0]["first_name"],
                "last_name": result[0]["last_name"],
                "email": result[0]["email"],
                "password": result[0]["password"],
                "created_at": result[0]["users.created_at"],
                "updated_at": result[0]["users.updated_at"]
            }
            owner=user.User(user_data)
            watchlist.owner = owner
            return watchlist
        return False