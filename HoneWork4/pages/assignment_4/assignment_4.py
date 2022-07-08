import requests
from flask import Blueprint, render_template
from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import os

assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         template_folder='templates')


@assignment_4.route('/assignment_4')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list)


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='Vbgkvht767!',
                                         database='project_db')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    data = 'select * from users'
    users_list = interact_db(data, query_type='fetch')
    email = request.form['email']
    for user in users_list:
        if email == user.email:
            print(email)
            return render_template('assignment_4.html', registration_message='The user exists in the system!',
                                   users=users_list)
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']
    query = "INSERT INTO users(name, password, email, phone) VALUES ('%s','%s','%s','%s')" % (
    name, password, email, phone)
    print(f' {name} {email} {password} {phone}')
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')


@assignment_4.route("/validation_user", methods=['POST'])
def validation_user():
    data = 'select * from users'
    users_list = interact_db(data, query_type='fetch')
    email = request.form['email']
    password = request.form['password']
    for user in users_list:
        if email == user.email:
            if password == user.password:
                user_id = user.id
                print(user_id)
                return render_template('assignment_4.html', v_id=user_id, users=users_list)
            else:
                return render_template('assignment_4.html', validation_message="Wrong password!", users=users_list)

    return render_template('assignment_4.html', validation_message="User not found!!", users=users_list)


@assignment_4.route("/update_email", methods=['POST'])
def update_email():
    user_id = request.form['user_id']
    email = request.form['email']
    query = "UPDATE users \
            SET Email= '%s' \
            WHERE id= '%s';" % (email, user_id)
    interact_db(query=query, query_type='commit')
    data = 'select * from users'
    users_list = interact_db(data, query_type='fetch')
    return render_template('assignment_4.html', validation_message="Email changed successfully!", users=users_list)


@assignment_4.route("/update_password", methods=['POST'])
def update_password():
    data = 'select * from users'
    users_list = interact_db(data, query_type='fetch')
    user_id = request.form['user_id']
    password = request.form['password']
    query = "UPDATE users \
                SET password= '%s' \
                WHERE id= '%s';" % (password, user_id)
    interact_db(query=query, query_type='commit')
    return render_template('assignment_4.html', validation_message="Password changed successfully!", users=users_list)
    return render_template('assignment_4.html', validation_message="The passwords are not the same, please try again.",
                           users=users_list)


@assignment_4.route("/update_phone", methods=['POST'])
def update_song():
    user_id = request.form['user_id']
    phone = request.form['phone']
    query = "UPDATE users \
            SET phone= '%s' \
            WHERE id= '%s';" % (phone, user_id)
    interact_db(query=query, query_type='commit')
    data = 'select * from users'
    users_list = interact_db(data, query_type='fetch')
    return render_template('assignment_4.html', validation_message="Your phone has been updated!", users=users_list)


@assignment_4.route("/delete_user", methods=['POST'])
def delete_user():
    data = 'select * from users'
    users_list = interact_db(data, query_type='fetch')
    email = request.form['email']
    password = request.form['password']
    for user in users_list:
        if email == user.email:
            if password == user.password:
                query = "DELETE FROM users WHERE email= '%s';" % email
                interact_db(query, query_type='commit')
                return redirect('/assignment_4')
            else:
                return render_template('assignment_4.html', Deletion_message="Wrong password!", users=users_list)

    return render_template('assignment_4.html', Deletion_message="User not found", users=users_list)


@assignment_4.route('/assignment4/users')
def assignment4_users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return_list = []
    for user in users_list:
        user_dict1 = {
            'name': user.name,
            'password': user.password,
            'email': user.email,
            'phone': user.phone
        }
        return_list.append(user_dict1)
    return jsonify(return_list)


@assignment_4.route('/assignment4/outer_source')
def outer_source():
    print("outer_source")
    return render_template('outer_source.html')


@assignment_4.route('/fetch_be')
def fetch_be():
    if 'type' in request.args:
        print('after click')
        user_id = request.args['user_id']
        users = []
        res = requests.get('https://reqres.in/api/users/' + user_id)
        users.append(res.json())

        user_dict1 = {
            'first_name': users[0]['data']['first_name'],
            'last_name': users[0]['data']['last_name'],
            'email': users[0]['data']['email'],
            'avatar': users[0]['data']['avatar'],
        }

    return render_template('outer_source.html', name=user_dict1['first_name'],
                           password=user_dict1['last_name'],
                           email=user_dict1['email'],
                           avatar=user_dict1['avatar'])


@assignment_4.route('/assignment4/restapi_users', defaults={'USER_ID': 5})
@assignment_4.route('/assignment4/restapi_users/<int:USER_ID>')
def restapi_users(USER_ID):
    query = f'select * from users where id={USER_ID}'
    users_list = interact_db(query, query_type='fetch')

    if len(users_list) == 0:
        return_dict = {
            'message': f'user {USER_ID} not found'
        }
    else:
        users_list = users_list[0]
        return_dict = {'name': users_list.name,
                       'password': users_list.password,
                       'email': users_list.email,
                       'phone': users_list.phone}
    return jsonify(return_dict)
