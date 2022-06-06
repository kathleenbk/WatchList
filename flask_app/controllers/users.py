from flask_app import app
from flask import render_template, session,flash,redirect, request
from flask_app.models.user import User
from flask_app.models.watchlist import Watchlist
import requests

import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/login_register')
def login_register():
    return render_template("login_register.html")



# Create new user
@app.route('/register', methods=['POST'])
def register():
    # Validate registration
    is_valid = User.validate(request.form)
    if not is_valid:
        return redirect('/login_register')
    
    # If registration is valid, save
    new = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(new)
    if not id:
        flash("Email already in use")
        return redirect('/')
    session['user_id'] = id
    return redirect('/home')


# User Login
@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)

# Check if user is in db and if password is correct
    if not user_in_db:
        flash("Incorrect Email/Password", "login")
        return redirect("/login_register")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Incorrect Email/Password", "login")
        return redirect('/login_register')

# Log user in
    session['user_id'] = user_in_db.id
    return redirect('/home')

# User Page
@app.route('/home')
def home():
    if 'user_id' in session:
        
        data={
            "id":session['user_id']

        }
        user=User.get_one(data)
        
        # watchlists=Watchlist.get_all_watchlists()
        watchlists=Watchlist.get_user_watchlists(data)
        return render_template("home.html", watchlists=watchlists, user=user)
    if not 'user_id' in session:
        return redirect('/')

# Logout, clears session
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/browsemovies')
def browsemovies():
    return render_template('browse.html', )

@app.route('/browse', methods=['GET'])
def browse():
    if 'user_id' in session:
        
        data={
            "id":session['user_id']

        }
        user=User.get_one(data)

        url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

        querystring = {
            "term":request.args['term']
        }

        headers = {
            "X-RapidAPI-Host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "3269c92d4dmshf47a0752a75c60bp15adc2jsn4c415fa71af2"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
    
        if response:
            # return response.json()
            results = response.json()["results"]
            length= len(results)
            
            
            if length>20:
                length=20
            return render_template('results.html', response=results, user=user, length=length)
        return redirect('/browse')
    if not 'user_id' in session:
        return redirect('/')

