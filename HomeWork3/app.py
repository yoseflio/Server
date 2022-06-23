from flask import Flask, redirect, render_template
from flask import url_for
from datetime import timedelta
from flask import request, session, jsonify

app = Flask(__name__)
app.secret_key = '1231'
app.config['SESSION_PERMANENT'] = True
app.config['permanent_session_lifetime'] = timedelta(minutes=20)

user_dict = {
    'user1': {'name': 'LiorYosef', 'password': '7676', 'email': 'lioryosef96@gmail.com',
              'PhoneNumber': '0546321241'},
    'user2': {'name': 'matandabush', 'password': '6767', 'email': 'matandabush@gmail.com',
              'PhoneNumber': '0545484971'},
    'user3': {'name': 'OmerMor', 'password': '1111', 'email': 'omermor@gmail.com',
              'PhoneNumber': '0544895984'},
    'user4': {'name': 'DorBaznak', 'password': '1234', 'email': 'Dorbaznak@gmail.com',
              'PhoneNumber': '054123456'},
    'user5': {'name': 'Netanel', 'password': '2222', 'email': 'Netanel@gmail.com',
              'PhoneNumber': '0587654321'}
}

catalog_dict = {
    'computer': 4000,
    'mouse': 100,
    'screen': 2000,
    'keyboard': 100,
}


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/contect')
def contect():
    return render_template("contect.html")



usersDetail = list(user_dict.values())

emails = []
for i in range(len(usersDetail)):
    userEmail = usersDetail[i]['email'].lower()
    emails.append(userEmail)
    print(userEmail)


def index_by_email(email):
    for i in range(len(emails)):
        if emails[i] == email:
            return i


@app.route('/log_in', methods=['GET', 'POST'])
def login_func():
    if request.method == 'POST':
        user_mail = request.form['Email'].lower()
        password = request.form['password']
        if user_mail in emails:
            index = index_by_email(user_mail)
            print(index)
            user_password = usersDetail[index]['password']
            if user_password == password:
                username = usersDetail[index]['name']
                PhoneNumber = usersDetail[index]['PhoneNumber']
                email = usersDetail[index]['email']
                session['PhoneNumber'] = PhoneNumber
                session['email'] = email
                session['name'] = username
                session['logedin'] = True
                return render_template('log_in.html',
                                       message='Success')
            else:
                return render_template('log_in.html',
                                       message='Wrong Password!')
        else:
            return render_template('log_in.html',
                                   message='Wrong Email!')
    session['logedin'] = False
    return render_template('log_in.html')


@app.route('/assignment3_1')
def catalog_func():
    if 'product_name' in request.args:
        product_name = request.args['product_name']
        if product_name == '':
            return render_template('assignment3_1.html',
                                   catalog_dict=catalog_dict)
        if product_name in catalog_dict:
            return render_template('assignment3_1.html',
                                   product_name=product_name,
                                   product_price=catalog_dict[product_name])
        else:
            return render_template('assignment3_1.html',
                                   message='Product not found.')
    return render_template('assignment3_1.html')


usersDetail = list(user_dict.values())

names = []
for i in range(len(usersDetail)):
    userName = usersDetail[i]['name'].lower()
    names.append(userName)
    print(userName)


def index_by_userName(name):
    for i in range(len(names)):
        if names[i] == name:
            return i


@app.route('/assignment3_2')
def assignment3_2():
    if request.method == 'GET':
        if 'Username' in request.args:
            Username = request.args['Username'].lower()
            if Username == '':
                return render_template('assignment3_2.html', user_dict=user_dict)
            if Username in names:
                IndexName = index_by_userName(Username)
                username = usersDetail[IndexName]['name']
                email = usersDetail[IndexName]['email']
                PhoneNumber = usersDetail[IndexName]['PhoneNumber']
                return render_template('assignment3_2.html', username=username, email=email, phone_number=PhoneNumber)
            else:
                return render_template('assignment3_2.html',
                                       message='Wrong Name!')
        else:
            return render_template('assignment3_2.html')
    return render_template('assignment3_2.html',
                           user_dict=user_dict)


@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('login_func'))


if __name__ == '__main__':
    app.run()