from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.user import User

@app.route('/')
def display_users():
    all_users = User.get_all()
    return render_template("all_users.html", all_users= all_users)

@app.route('/user/new')
def new_user():
    return render_template("new_user.html")

@app.route('/process', methods=["POST"])
def process_new_user():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
    }
    if not User.validate_user(request.form):
        return redirect('/user/new')
    new_user = User.create(data)
    return redirect(f'/user/show/{new_user}')

@app.route('/user/show/<int:user_id>')
def show_user(user_id):
    data = {
        'id' : user_id
    }
    user = User.get_one(data)
    return render_template('show_user.html', user = user)

@app.route('/user/edit/<int:user_id>')
def edit_user(user_id):
    data = {
        'id' : user_id
    }
    user = User.get_one(data)
    return render_template('edit_users.html', user=user)

@app.route('/user/update', methods=['POST'])
def update_user(user_id):
    User.update(request.form, user_id)
    return redirect('/user/show/<int:user_id>')

@app.route('/user/delete/<int:user_id>')
def delete_user(user_id):
    User.delete(user_id)
    return redirect('/')

