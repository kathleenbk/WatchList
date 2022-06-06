from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.watchlist import Watchlist
from flask_app.models.user import User
from flask_app.controllers import users


@app.route('/watchlists/new')
def new_watchlist():
    if 'user_id' in session:
        
        data={
            "id":session['user_id']
        }
        user=User.get_one(data)
        return render_template('newwatchlist.html', user=user)
    if not 'user_id' in session:
        return redirect ('/')

@app.route('/watchlists/create', methods=["POST"])
def create_watchlist():
    data = {
        'name':request.form['name'],
        'user_id':session['user_id']
    }
    Watchlist.save_watchlist(data)
    return redirect('/home')